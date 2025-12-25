import os
import json
from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from agent.graph import graph
from agent.schemas.state import GraphState
from api.schemas import ChatRequest, ChatResponse, FileUploadResponse

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

        return ChatResponse(
            answer=last_message.content
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
            
            # Stream events from the graph
            async for event in graph.astream(initial_state, stream_mode="updates"):
                # Extract the generate_response output
                if "generate_response" in event:
                    message = event["generate_response"]["messages"][-1]
                    content = message.content
                    
                    # Stream token-by-token (character by character)
                    for token in content:
                        yield f"data: {json.dumps({'token': token})}\n\n"
            
            # Send completion signal
            yield "data: {\"done\": true}\n\n"
            
        except Exception as e:
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
