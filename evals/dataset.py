"""Example dataset for evaluation."""

# Sample dataset for evaluation
EXAMPLE_DATASET = [
    {
        "question": "What is LangGraph?",
        "expected_answer": "A framework for building stateful agents",
    },
    {
        "question": "How do I create a graph?",
        "expected_answer": "Using StateGraph class",
    },
    {
        "question": "What is RAG?",
        "expected_answer": "Retrieval Augmented Generation",
    },
]


def get_evaluation_dataset():
    """Get evaluation dataset.
    
    Returns:
        List of evaluation examples
    """
    return EXAMPLE_DATASET
