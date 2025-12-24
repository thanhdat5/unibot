"""Chain functions for RAG operations."""

from langsmith import traceable

from agent.schemas import GraphState
from agent.config.prompts import RAG_PROMPT


@traceable(run_type="chain")
def format_rag_input(state: GraphState) -> dict:
    """Format inputs for RAG pipeline.
    
    Combines retrieved documents and conversation context into a formatted prompt.
    
    Args:
        state: Current graph state containing question, messages, and documents
        
    Returns:
        Dictionary containing formatted prompt and other necessary data
    """
    question = state["question"]
    documents = state["documents"]
    messages = state["messages"]
    
    formatted_docs = "\n\n".join(doc.page_content for doc in documents)
    rag_prompt_formatted = RAG_PROMPT.format(
        context=formatted_docs,
        conversation=messages,
        question=question
    )
    
    return {
        "prompt": rag_prompt_formatted,
        "question": question,
        "documents": documents
    }
