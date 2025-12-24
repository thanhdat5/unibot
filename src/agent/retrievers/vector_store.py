"""Vector store and retriever initialization."""

import os
import tempfile

from langchain_community.document_loaders.sitemap import SitemapLoader
from langchain_community.vectorstores import SKLearnVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from agent.config.settings import (
    VECTOR_STORE_PERSIST_DIR,
    VECTOR_STORE_SERIALIZER,
    SITEMAP_URL,
    DOCUMENT_CHUNK_SIZE,
    DOCUMENT_CHUNK_OVERLAP,
    RETRIEVER_LAMBDA_MULT,
)


def get_vector_db_retriever():
    """Initialize or load vector database retriever.
    
    Creates a new vector store from LangSmith documentation sitemap if it doesn't exist,
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

    # Otherwise, index documents and create new vector store
    sitemap_loader = SitemapLoader(
        web_path=SITEMAP_URL,
        continue_on_failure=True
    )
    documents = sitemap_loader.load()

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
