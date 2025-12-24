"""
# LangSmith Integration Guide

## Setup Instructions

### 1. Get API Key from LangSmith
- Go to https://smith.langchain.com
- Sign in or create an account
- Navigate to Settings > API Keys
- Copy your API key

### 2. Create `.env` File
```bash
cp .env.example .env
```

### 3. Add Your API Keys to `.env`
```
OPENAI_API_KEY=sk-...
LANGSMITH_API_KEY=ls_...
LANGSMITH_PROJECT=unibot-agent
LANGSMITH_TRACING_V2=true
```

### 4. Install Dependencies
```bash
pip install python-dotenv
```

## Features

### 1. Automatic Tracing (Monitoring)
All `@traceable` decorated functions automatically log to LangSmith when API key is configured.

**View traces:**
- Open LangGraph Studio: http://127.0.0.1:2024
- Dashboard will show all traced operations

### 2. Evaluations
```bash
# Run evaluations on the agent
python evals/run_evaluation.py
```

### 3. LangSmith Dashboard
Access monitoring and evaluation results:
- URL: https://smith.langchain.com
- Project: `unibot-agent`
- Tabs: Runs, Evaluations, Datasets, Monitoring

## Project Structure

```
evals/
├── __init__.py
├── evaluation.py      (evaluation functions)
├── dataset.py         (test datasets)
└── run_evaluation.py  (main evaluation script)

src/agent/config/
└── langsmith_config.py (LangSmith configuration)

LANGSMITH_SETUP.md (this file)
```

## Usage Example

### Basic Tracing
```python
from agent.config.langsmith_config import LANGSMITH_API_KEY
from agent.graph import graph

# Tracing is automatically enabled when LANGSMITH_API_KEY is set
result = graph.invoke({
    "question": "What is LangGraph?",
    "messages": [],
    "documents": []
})
```

### Custom Evaluation
```python
from langsmith import evaluate
from evals.evaluation import evaluate_relevance

# Define your evaluation logic
```

## Monitoring & Evaluation Metrics

### Built-in Evaluators
- **relevance**: Checks if documents were retrieved
- **response_quality**: Verifies response was generated
- **answer_length**: Validates answer has reasonable length

### Add Custom Evaluators
```python
from langsmith.evaluation import EvaluationResult

def my_evaluator(run, example):
    score = 1 if condition else 0
    return EvaluationResult(
        key="my_metric",
        score=score
    )
```

## Troubleshooting

### Issue: No traces appearing in LangSmith
**Solution:**
- Verify LANGSMITH_API_KEY is set in `.env` file
- Restart `langgraph dev` server
- Check that `LANGSMITH_TRACING_V2=true`

### Issue: "Authentication failed"
**Solution:**
- Double-check API key is correct
- Ensure no quotes around API key in `.env`
- Regenerate API key in LangSmith dashboard

### Issue: Traces not showing in LangGraph Studio
**Solution:**
- Verify `baseUrl` parameter is correct
- Check firewall/proxy settings
- Restart the development server

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `LANGSMITH_API_KEY` | Your LangSmith API key | `ls_abc123xyz...` |
| `LANGSMITH_PROJECT` | Project name in LangSmith | `unibot-agent` |
| `LANGSMITH_TRACING_V2` | Enable tracing v2 | `true` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-abc123xyz...` |

## Resources

- [LangSmith Documentation](https://docs.smith.langchain.com)
- [LangSmith Evaluation Guide](https://docs.smith.langchain.com/evaluation)
- [LangSmith Monitoring](https://docs.smith.langchain.com/monitoring)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

## Next Steps

1. Set up `.env` file with your API keys
2. Run `langgraph dev` to start the development server
3. Open https://smith.langchain.com to view your project
4. Test the agent and monitor traces in real-time
5. Run evaluations to assess agent performance
"""
