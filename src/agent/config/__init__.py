"""Configuration module for the agent."""

from .prompts import RAG_PROMPT
from .settings import (
    LLM_MODEL_NAME,
    LLM_TEMPERATURE,
    VECTOR_STORE_PERSIST_DIR,
    DOCS_DIR,
    DOCUMENT_CHUNK_SIZE,
    DOCUMENT_CHUNK_OVERLAP,
    RETRIEVER_LAMBDA_MULT,
)

__all__ = [
    "RAG_PROMPT",
    "LLM_MODEL_NAME",
    "LLM_TEMPERATURE",
    "VECTOR_STORE_PERSIST_DIR",
    "DOCS_DIR",
    "DOCUMENT_CHUNK_SIZE",
    "DOCUMENT_CHUNK_OVERLAP",
    "RETRIEVER_LAMBDA_MULT",
]
