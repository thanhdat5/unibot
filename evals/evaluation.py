"""LangSmith evaluation functions."""

from langsmith import Client, evaluate
from langsmith.evaluation import EvaluationResult
from langchain_core.messages import HumanMessage


def evaluate_relevance(run, example):
    """Evaluate if retrieved documents are relevant to the question.
    
    Args:
        run: LangSmith run object
        example: Example from dataset
        
    Returns:
        EvaluationResult with score
    """
    score = 1 if "documents" in run.outputs else 0
    return EvaluationResult(
        key="relevance",
        score=score,
    )


def evaluate_response_quality(run, example):
    """Evaluate quality of generated response.
    
    Args:
        run: LangSmith run object
        example: Example from dataset
        
    Returns:
        EvaluationResult with score
    """
    if not run.outputs:
        return EvaluationResult(key="response_quality", score=0)
    
    messages = run.outputs.get("messages", [])
    has_response = len(messages) > 0
    score = 1 if has_response else 0
    
    return EvaluationResult(
        key="response_quality",
        score=score,
    )


def evaluate_answer_length(run, example):
    """Evaluate if answer has reasonable length.
    
    Args:
        run: LangSmith run object
        example: Example from dataset
        
    Returns:
        EvaluationResult with score
    """
    if not run.outputs:
        return EvaluationResult(key="answer_length", score=0)
    
    messages = run.outputs.get("messages", [])
    if len(messages) > 0:
        last_message = messages[-1]
        content = last_message.content if hasattr(last_message, 'content') else str(last_message)
        # Score based on length (aim for 50-500 characters)
        length = len(str(content))
        score = 1 if 50 <= length <= 500 else 0.5
    else:
        score = 0
    
    return EvaluationResult(
        key="answer_length",
        score=score,
    )
