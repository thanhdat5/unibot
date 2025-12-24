from fastapi import APIRouter, HTTPException
from agent.graph import graph
from agent.schemas.state import GraphState
from api.schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["Chat"])

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
