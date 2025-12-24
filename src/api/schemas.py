from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., example="Thời gian làm việc chính thức của HipLab là như thế nào?")


class ChatResponse(BaseModel):
    answer: str
