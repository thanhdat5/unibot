import os
import json
from pathlib import Path

# MUST be imported first to enable LangSmith tracing
import agent.config.langsmith_config  # noqa: F401

from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse, FileResponse
from agent.graph import graph
from agent.schemas.state import GraphState
from api.schemas import ChatRequest, ChatResponse, FileUploadResponse, DocumentReference
from langchain_openai import ChatOpenAI
from agent.config import LLM_MODEL_NAME, LLM_TEMPERATURE
from langsmith import trace
from langsmith.run_trees import RunTree

router = APIRouter(prefix="/chat", tags=["Chat"])

# Folder paths
DOCS_FOLDER = Path(__file__).parent.parent / "docs"
ALLOWED_EXTENSIONS = {".txt", ".pdf", ".docx"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        initial_state: GraphState = {
            "question": req.question,
            "messages": [],
            "documents": [],
        }

        final_state = await graph.ainvoke(initial_state)

        last_message = final_state["messages"][-1]
        
        # Extract unique documents from retrieved documents
        retrieved_docs = []
        seen_sources = set()
        
        for doc in final_state.get("documents", []):
            source = doc.metadata.get("source", "")
            if source and source not in seen_sources:
                seen_sources.add(source)
                # Extract filename from source path
                filename = Path(source).name
                retrieved_docs.append(
                    DocumentReference(
                        filename=filename,
                        source=source,
                        page=doc.metadata.get("page", None)
                    )
                )

        return ChatResponse(
            answer=last_message.content,
            documents=retrieved_docs
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stream")
async def chat_stream(req: ChatRequest):
    """Streaming chat endpoint using Server-Sent Events with token-by-token streaming"""
    
    async def generate():
        from agent.nodes.generation import call_openai_stream
        from agent.config.prompts import RAG_PROMPT
        from langsmith.run_trees import RunTree
        
        # Initialize LLM
        llm = ChatOpenAI(model_name=LLM_MODEL_NAME, temperature=LLM_TEMPERATURE)
        
        initial_state: GraphState = {
            "question": req.question,
            "messages": [],
            "documents": [],
        }
        
        # Create a run tree to track this operation
        run_tree = RunTree(
            name="chat_stream",
            run_type="chain",
            inputs={"question": req.question},
        )
        
        try:
            # First, run the full graph to get documents and prepare for streaming
            final_state = await graph.ainvoke(initial_state)
            
            # Get documents from retrieval
            documents = final_state.get("documents", [])
            
            # Format documents for context
            formatted_docs = "\n\n".join(doc.page_content for doc in documents)
            
            # Prepare the prompt
            rag_prompt_formatted = RAG_PROMPT.format(
                context=formatted_docs,
                conversation=initial_state["messages"],
                question=req.question
            )
            
            # Collect full response for tracing
            full_response = ""
            
            # Stream the response token by token
            async for token in call_openai_stream(rag_prompt_formatted, llm):
                full_response += token
                yield f"data: {json.dumps({'token': token})}\n\n"
            
            # Send documents list AFTER response
            if documents:
                retrieved_docs = []
                seen_sources = set()
                
                for doc in documents:
                    source = doc.metadata.get("source", "")
                    if source and source not in seen_sources:
                        seen_sources.add(source)
                        filename = Path(source).name
                        retrieved_docs.append({
                            "filename": filename,
                            "source": source,
                            "page": doc.metadata.get("page", None)
                        })
                
                if retrieved_docs:
                    yield f"data: {json.dumps({'documents': retrieved_docs})}\n\n"
            
            # Send completion signal
            yield "data: {\"done\": true}\n\n"
            
            # Update run tree with outputs
            run_tree.end(outputs={
                "response": full_response,
                "documents": retrieved_docs if documents else []
            })
            run_tree.post()
            
        except Exception as e:
            print(f"[ERROR] {str(e)}")  # Debug
            run_tree.end(error=str(e))
            run_tree.post()
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive"
        }
    )


router_upload = APIRouter(prefix="/upload", tags=["Upload"])


@router_upload.post("/file", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """Upload file (.txt, .pdf, .docx) to src/docs folder"""
    try:
        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format. Supported formats: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Create docs folder if it doesn't exist
        DOCS_FOLDER.mkdir(parents=True, exist_ok=True)
        
        # Read file content
        content = await file.read()
        
        # Check file size
        file_size = len(content)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File is too large. Maximum limit: {MAX_FILE_SIZE / 1024 / 1024}MB"
            )
        
        # Save file
        file_path = DOCS_FOLDER / file.filename
        with open(file_path, "wb") as f:
            f.write(content)
        
        return FileUploadResponse(
            filename=file.filename,
            file_path=str(file_path),
            file_size=file_size,
            message=f"File '{file.filename}' uploaded successfully"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload error: {str(e)}")


@router_upload.get("/documents")
async def list_documents():
    """List all documents in the docs folder"""
    try:
        if not DOCS_FOLDER.exists():
            return {"documents": []}
        
        documents = []
        for file_path in DOCS_FOLDER.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in ALLOWED_EXTENSIONS:
                documents.append({
                    "filename": file_path.name,
                    "file_size": file_path.stat().st_size,
                    "created_at": file_path.stat().st_ctime,
                    "modified_at": file_path.stat().st_mtime
                })
        
        return {"documents": sorted(documents, key=lambda x: x["filename"])}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")


@router_upload.get("/documents/{filename}")
async def download_document(filename: str):
    """Download a document by filename"""
    try:
        # Security: prevent directory traversal
        if ".." in filename or "/" in filename or "\\" in filename:
            raise HTTPException(status_code=400, detail="Invalid filename")
        
        file_path = DOCS_FOLDER / filename
        
        # Verify file exists and is in allowed folder
        if not file_path.exists() or not file_path.is_file():
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Verify file extension is allowed
        if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail="File format not allowed")
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type="application/octet-stream"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading document: {str(e)}")


@router_upload.delete("/documents/{filename}")
async def delete_document(filename: str):
    """Delete a document by filename"""
    try:
        # Security: prevent directory traversal
        if ".." in filename or "/" in filename or "\\" in filename:
            raise HTTPException(status_code=400, detail="Invalid filename")
        
        file_path = DOCS_FOLDER / filename
        
        # Verify file exists and is in allowed folder
        if not file_path.exists() or not file_path.is_file():
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Verify file extension is allowed
        if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail="File format not allowed")
        
        # Delete the file
        file_path.unlink()
        
        return {
            "message": f"Document '{filename}' deleted successfully",
            "filename": filename
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")
