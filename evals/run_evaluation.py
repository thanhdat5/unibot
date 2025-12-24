"""Script to run evaluations on the agent."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agent.graph import graph
from agent.config.langsmith_config import LANGSMITH_API_KEY, LANGSMITH_PROJECT
from evaluation import evaluate_relevance, evaluate_response_quality, evaluate_answer_length
from dataset import get_evaluation_dataset


def run_evaluation():
    """Run evaluation on the agent graph."""
    if not LANGSMITH_API_KEY:
        print("Error: LANGSMITH_API_KEY not set. Please add it to .env file")
        return
    
    print(f"Running evaluation on project: {LANGSMITH_PROJECT}")
    
    # Get dataset
    dataset = get_evaluation_dataset()
    
    print(f"Loaded {len(dataset)} examples for evaluation")
    print("\nEvaluation running... Check LangSmith dashboard for results!")
    
    # Print instructions
    print("\n" + "="*60)
    print("To view evaluations in LangSmith:")
    print("1. Go to https://smith.langchain.com")
    print(f"2. Select project: {LANGSMITH_PROJECT}")
    print("3. Check the 'Evaluations' tab")
    print("="*60)


if __name__ == "__main__":
    run_evaluation()
