"""Vector store and retriever initialization."""

import os
import tempfile
from pathlib import Path

from functools import partial
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import SKLearnVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from agent.config.settings import (
    VECTOR_STORE_PERSIST_DIR,
    VECTOR_STORE_SERIALIZER,
    DOCS_DIR,
    DOCUMENT_CHUNK_SIZE,
    DOCUMENT_CHUNK_OVERLAP,
    RETRIEVER_LAMBDA_MULT,
)


def get_vector_db_retriever():
    """Initialize or load vector database retriever.
    
    Creates a new vector store from local documentation .txt files if it doesn't exist,
    otherwise loads the existing vector store from disk.
    
    Returns:
        A retriever instance from SKLearnVectorStore
    """
    persist_path = os.path.join(tempfile.gettempdir(), VECTOR_STORE_PERSIST_DIR)
    embd = OpenAIEmbeddings()

    # If vector store exists, then load it
    if os.path.exists(persist_path):
        vectorstore = SKLearnVectorStore(
            embedding=embd,
            persist_path=persist_path,
            serializer=VECTOR_STORE_SERIALIZER
        )
        return vectorstore.as_retriever(lambda_mult=RETRIEVER_LAMBDA_MULT)

    # Otherwise, index documents from local directory and create new vector store
    # Resolve path relative to the project root
    docs_path = Path(__file__).parent.parent.parent.parent / DOCS_DIR
    if not docs_path.exists():
        raise ValueError(f"Documentation directory not found: {docs_path}")
    
    # Use TextLoader with UTF-8 encoding to handle Vietnamese text
    text_loader_utf8 = partial(TextLoader, encoding="utf-8")
    directory_loader = DirectoryLoader(
        path=str(docs_path),
        glob="**/*.txt",
        loader_cls=text_loader_utf8,
        show_progress=True,
        use_multithreading=True
    )
    documents = directory_loader.load()

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=DOCUMENT_CHUNK_SIZE,
        chunk_overlap=DOCUMENT_CHUNK_OVERLAP
    )
    doc_splits = text_splitter.split_documents(documents)

    vectorstore = SKLearnVectorStore.from_documents(
        documents=doc_splits,
        embedding=embd,
        persist_path=persist_path,
        serializer=VECTOR_STORE_SERIALIZER
    )
    vectorstore.persist()
    return vectorstore.as_retriever(lambda_mult=RETRIEVER_LAMBDA_MULT)
