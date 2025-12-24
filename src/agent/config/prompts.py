"""Prompt templates for RAG agent."""

RAG_PROMPT = """You are an assistant for question-answering tasks.

Use the following pieces of retrieved context to answer the question.

Context:
{context}

Conversation history:
{conversation}

Question: {question}

Answer:"""
