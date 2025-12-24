"""Document retrieval node for the agent graph."""

from langchain_core.messages import get_buffer_string
from langsmith import traceable

from agent.schemas import GraphState


@traceable(run_type="chain")
def retrieve_documents(state: GraphState, retriever):
    """Retrieve relevant documents from vectorstore based on conversation context.
    
    Fetches documents relevant to the user's question combined with message history.
    
    Args:
        state: Current graph state
        retriever: Retriever instance for document retrieval
        
    Returns:
        Updated state with retrieved documents
    """
    messages = state.get("messages", [])
    question = state["question"]
    documents = retriever.invoke(f"{get_buffer_string(messages)} {question}")
    return {"documents": documents}
