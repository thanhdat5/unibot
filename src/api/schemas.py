from pydantic import BaseModel, Field
from typing import List, Optional


class ChatRequest(BaseModel):
    question: str = Field(..., example="Thời gian làm việc chính thức của HipLab là như thế nào?")


class DocumentReference(BaseModel):
    """Retrieved document reference"""
    filename: str = Field(..., description="Document filename")
    source: Optional[str] = Field(None, description="Document source path")
    page: Optional[int] = Field(None, description="Page number if applicable")


class ChatResponse(BaseModel):
    answer: str
    documents: Optional[List[DocumentReference]] = Field(default_factory=list, description="Retrieved documents")


class FileUploadResponse(BaseModel):
    filename: str = Field(..., description="Uploaded filename")
    file_path: str = Field(..., description="File path where the file is saved")
    file_size: int = Field(..., description="File size in bytes")
    message: str = Field(..., description="Upload result message")
