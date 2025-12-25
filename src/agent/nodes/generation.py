"""Response generation node for the agent graph."""

from langchain_core.messages import HumanMessage
from langsmith import traceable

from agent.schemas import GraphState
from agent.config.prompts import RAG_PROMPT


@traceable(run_type="chain")
def generate_response(state: GraphState, llm) -> dict:
    """Generate a response using retrieved documents and conversation context.
    
    Formats context and conversation history, then calls LLM to generate an answer.
    
    Args:
        state: Current graph state
        llm: Language model instance
        
    Returns:
        Updated state with generated response added to messages
    """
    question = state["question"]
    messages = state["messages"]
    documents = state["documents"]
    
    formatted_docs = "\n\n".join(doc.page_content for doc in documents)
    
    rag_prompt_formatted = RAG_PROMPT.format(
        context=formatted_docs,
        conversation=messages,
        question=question
    )
    generation = call_openai(rag_prompt_formatted, llm)
    return {"documents": documents, "messages": [HumanMessage(question), generation]}


@traceable(run_type="llm")
def call_openai(prompt: str, llm):
    """Call OpenAI LLM with the formatted RAG prompt.
    
    Returns the chat completion output from OpenAI.
    
    Args:
        prompt: Formatted prompt for the LLM
        llm: Language model instance
        
    Returns:
        Generated response from the LLM
    """
    return llm.invoke([HumanMessage(content=prompt)])


@traceable(run_type="llm")
async def call_openai_stream(prompt: str, llm):
    """Stream response from OpenAI LLM.
    
    Yields tokens/chunks from the LLM response.
    
    Args:
        prompt: Formatted prompt for the LLM
        llm: Language model instance
        
    Yields:
        Token/chunk strings from the LLM
    """
    async for chunk in llm.astream([HumanMessage(content=prompt)]):
        if hasattr(chunk, 'content') and chunk.content:
            yield chunk.content
