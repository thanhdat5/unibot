import os
import json
from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse, FileResponse
from agent.graph import graph
from agent.schemas.state import GraphState
from api.schemas import ChatRequest, ChatResponse, FileUploadResponse, DocumentReference

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
        try:
            initial_state: GraphState = {
                "question": req.question,
                "messages": [],
                "documents": [],
            }
            
            final_documents = None
            
            # Stream events from the graph
            async for event in graph.astream(initial_state, stream_mode="updates"):
                print(f"[STREAM EVENT] Keys: {event.keys()}")  # Debug
                
                # Extract the generate_response output
                if "generate_response" in event:
                    message = event["generate_response"]["messages"][-1]
                    content = message.content
                    
                    # Stream token-by-token (character by character)
                    for token in content:
                        yield f"data: {json.dumps({'token': token})}\n\n"
                
                # Store final documents state from any node that updates it
                for node_name, node_data in event.items():
                    if isinstance(node_data, dict) and "documents" in node_data:
                        final_documents = node_data["documents"]
                        print(f"[DOCUMENTS] Found {len(final_documents)} docs from {node_name}")  # Debug
            
            print(f"[FINAL STATE] Documents: {final_documents}")  # Debug
            
            # Send documents list BEFORE completion signal
            if final_documents:
                retrieved_docs = []
                seen_sources = set()
                
                for doc in final_documents:
                    source = doc.metadata.get("source", "")
                    if source and source not in seen_sources:
                        seen_sources.add(source)
                        filename = Path(source).name
                        retrieved_docs.append({
                            "filename": filename,
                            "source": source,
                            "page": doc.metadata.get("page", None)
                        })
                
                print(f"[SENDING] {len(retrieved_docs)} documents to client")  # Debug
                if retrieved_docs:
                    yield f"data: {json.dumps({'documents': retrieved_docs})}\n\n"
            
            # Send completion signal AFTER documents
            yield "data: {\"done\": true}\n\n"
            
        except Exception as e:
            print(f"[ERROR] {str(e)}")  # Debug
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
