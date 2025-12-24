"""State definitions for the agent graph."""

import operator
from typing import Annotated, List

from langchain_core.documents import Document
from langchain_core.messages import AnyMessage
from typing_extensions import TypedDict


class GraphState(TypedDict):
    """State for the RAG agent graph.
    
    Attributes:
        question: User's question or input
        messages: Conversation history with cumulative messages
        documents: Retrieved documents from vectorstore
    """
    question: str
    messages: Annotated[List[AnyMessage], operator.add]
    documents: List[Document]
