"""Configuration and settings for the agent."""

# LLM Configuration
LLM_MODEL_NAME = "gpt-4o-mini"
LLM_TEMPERATURE = 0

# Vector Store Configuration
VECTOR_STORE_PERSIST_DIR = "union.parquet"
VECTOR_STORE_SERIALIZER = "parquet"

# Document Loading Configuration
DOCS_DIR = "src/docs"
DOCUMENT_CHUNK_SIZE = 500
DOCUMENT_CHUNK_OVERLAP = 0

# Retriever Configuration
RETRIEVER_LAMBDA_MULT = 0
