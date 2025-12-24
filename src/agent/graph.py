import nest_asyncio
from functools import partial

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

from agent.schemas import GraphState
from agent.nodes import retrieve_documents, generate_response
from agent.retrievers import get_vector_db_retriever
from agent.config import LLM_MODEL_NAME, LLM_TEMPERATURE

nest_asyncio.apply()

# Initialize components
retriever = get_vector_db_retriever()
llm = ChatOpenAI(model_name=LLM_MODEL_NAME, temperature=LLM_TEMPERATURE)


def build_graph():
    """Build and compile the RAG agent graph.
    
    Returns:
        Compiled LangGraph graph instance
    """
    # Create graph builder
    graph_builder = StateGraph(GraphState)
    
    # Add nodes with bound resources
    graph_builder.add_node(
        "retrieve_documents",
        partial(retrieve_documents, retriever=retriever)
    )
    graph_builder.add_node(
        "generate_response",
        partial(generate_response, llm=llm)
    )
    
    # Add edges
    graph_builder.add_edge(START, "retrieve_documents")
    graph_builder.add_edge("retrieve_documents", "generate_response")
    graph_builder.add_edge("generate_response", END)
    
    # Compile and return
    return graph_builder.compile()


# Create the graph instance
graph = build_graph()