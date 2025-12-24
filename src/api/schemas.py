from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., example="Thời gian làm việc chính thức của HipLab là như thế nào?")


class ChatResponse(BaseModel):
    answer: str


class FileUploadResponse(BaseModel):
    filename: str = Field(..., description="Uploaded filename")
    file_path: str = Field(..., description="File path where the file is saved")
    file_size: int = Field(..., description="File size in bytes")
    message: str = Field(..., description="Upload result message")
