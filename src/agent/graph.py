import nest_asyncio
import operator
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AnyMessage, get_buffer_string
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from typing import List
from typing_extensions import TypedDict, Annotated
from agent.utils import get_vector_db_retriever, RAG_PROMPT
from langsmith import traceable

nest_asyncio.apply()

retriever = get_vector_db_retriever()
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

# Define Graph state
class GraphState(TypedDict):
    question: str
    messages: Annotated[List[AnyMessage], operator.add]
    documents: List[Document]

@traceable(run_type="chain")
def retrieve_documents(state: GraphState):
    """Retrieve relevant documents from vectorstore based on conversation context.
    
    Fetches documents relevant to the user's question combined with message history.
    """
    messages = state.get("messages", [])
    question = state["question"]
    documents = retriever.invoke(f"{get_buffer_string(messages)} {question}")
    return {"documents": documents}

@traceable(run_type="chain")
def generate_response(state: GraphState):
    """Generate a response using retrieved documents and conversation context.
    
    Formats context and conversation history, then calls LLM to generate an answer.
    """
    question = state["question"]
    messages = state["messages"]
    documents = state["documents"]
    formatted_docs = "\n\n".join(doc.page_content for doc in documents)
    
    rag_prompt_formatted = RAG_PROMPT.format(context=formatted_docs, conversation=messages, question=question)
    generation = call_openai(rag_prompt_formatted)
    return {"documents": documents, "messages": [HumanMessage(question), generation]}


@traceable(run_type="llm")
def call_openai(prompt: str):
    """Call OpenAI LLM with the formatted RAG prompt.
    
    Returns the chat completion output from OpenAI.
    """
    return llm.invoke([HumanMessage(content=prompt)])


# Define Graph
graph_builder = StateGraph(GraphState)
graph_builder.add_node("retrieve_documents", retrieve_documents)
graph_builder.add_node("generate_response", generate_response)
graph_builder.add_edge(START, "retrieve_documents")
graph_builder.add_edge("retrieve_documents", "generate_response")
graph_builder.add_edge("generate_response", END)

graph = graph_builder.compile()