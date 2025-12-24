"""Configuration for LangSmith integration."""

import os
from dotenv import load_dotenv

load_dotenv()

# LangSmith Configuration
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "unibot-agent")
LANGSMITH_TRACING_V2 = os.getenv("LANGSMITH_TRACING_V2", "true").lower() == "true"

# Set environment variables for LangSmith
if LANGSMITH_API_KEY:
    os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
    os.environ["LANGSMITH_PROJECT"] = LANGSMITH_PROJECT
    os.environ["LANGSMITH_TRACING_V2"] = str(LANGSMITH_TRACING_V2)
