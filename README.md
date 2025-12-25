# UniBot - HipLab Chat Assistant

A production-ready RAG (Retrieval Augmented Generation) chatbot powered by LangGraph, FastAPI, and modern web technologies. UniBot specializes in answering questions about HipLab internal policies, regulations, and employee benefits through an intelligent streaming chat interface.

## 🚀 Key Features

- **LangGraph-Powered RAG Pipeline**: Advanced agent orchestration with retrieval and generation nodes
- **Real-time Streaming**: Token-by-token response streaming using Server-Sent Events (SSE)
- **Vector Database Integration**: Efficient document retrieval using vector embeddings
- **Modern Web Interface**: Responsive HTML/CSS/JavaScript frontend with real-time chat UI
- **Evaluation Framework**: Built-in dataset and evaluation utilities for RAG quality assessment
- **CORS-Enabled API**: Cross-origin support for seamless frontend-backend integration

## 📁 Folder Structure

```
unibot/
├── src/
│   ├── agent/                      # LangGraph agent & RAG logic
│   │   ├── graph.py               # Main LangGraph definition
│   │   ├── chains/                # LangChain components (RAG chain)
│   │   ├── config/                # Configuration (LLM, prompts, settings)
│   │   ├── nodes/                 # Graph nodes (retrieval, generation)
│   │   ├── retrievers/            # Vector store & retrieval logic
│   │   └── schemas/               # Data models (GraphState)
│   ├── api/                        # FastAPI REST API
│   │   ├── main.py               # API application & CORS setup
│   │   ├── routes.py             # Chat endpoints (/chat, /chat/stream)
│   │   └── schemas.py            # Request/response models
│   ├── web/                        # Frontend (HTML/CSS/JS)
│   │   ├── index.html            # Chat UI
│   │   ├── styles.css            # Styling & animations
│   │   └── app.js                # Client logic & streaming handler
│   └── docs/                       # Internal documentation & policies
├── tests/                          # Test suite
│   ├── unit_tests/               # Unit tests
│   └── integration_tests/        # Integration tests
├── pyproject.toml                  # Project metadata & dependencies
├── Makefile                        # Build & development commands
├── langgraph.json                  # LangGraph configuration
├── LANGSMITH_SETUP.md             # LangSmith integration guide
├── CODE_REVIEW.md                 # Code review guidelines
└── LICENSE
```

### Key Folder Responsibilities

- **src/agent/**: Contains the LangGraph workflow definition, RAG chain, and document retrieval logic
- **src/api/**: FastAPI server with streaming chat endpoints and CORS middleware
- **src/web/**: Self-contained static web application with real-time streaming support
- **src/docs/**: Internal policy documents used as RAG knowledge base

## 📋 Prerequisites

- **Python**: 3.9 or higher
- **pip**: Package manager (comes with Python)
- **Modern Web Browser**: Chrome, Firefox, Safari, or Edge (for frontend)

## 🔧 Installation Guide

### 1. Clone the Repository

```bash
git clone <repository-url>
cd unibot
```

### 2. Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -e .
```

This installs all project dependencies defined in `pyproject.toml`.

### 4. Environment Configuration

Create a `.env` file in the project root for API keys and configuration:

```env
# LLM Configuration
OPENAI_API_KEY=your-api-key-here
LLM_MODEL_NAME=gpt-4
LLM_TEMPERATURE=0.7

# LangSmith (Optional)
LANGSMITH_API_KEY=your-langsmith-key
LANGSMITH_PROJECT=unibot

# Vector Store (Optional)
VECTOR_STORE_URL=http://localhost:6333
```

## 🧠 Running LangGraph (Development Mode)

LangGraph Dev Server is useful for local development, debugging, and testing the graph flows interactively.

### Command

```bash
langgraph dev
```

### What It Does

- Launches a local LangGraph development server
- Provides interactive debugging interface
- Allows step-by-step execution of graph nodes
- Visualizes agent workflow in real-time

### Default Access

- **LangGraph Studio**: http://localhost:8000/

### Usage

Use LangGraph Studio to:
- Visualize the RAG pipeline
- Test individual nodes
- Debug graph execution
- Monitor state transitions

## 🔌 Running the API (FastAPI)

The FastAPI server exposes REST endpoints for chat and file upload operations.

### Command

```bash
uvicorn src.api.main:app --reload
```

**Note**: Working directory should be the project root (`unibot/`)

### What It Does

- Starts the FastAPI application server
- Enables auto-reload on code changes (development mode)
- Sets up CORS middleware for cross-origin requests
- Initializes LangGraph agent and vector store retriever

### Default Configuration

- **Host**: `127.0.0.1`
- **Port**: `8000`
- **API Base URL**: `http://localhost:8000`

### Available Endpoints

#### 1. **Chat Endpoint (Non-Streaming)**

```
POST /chat
Content-Type: application/json

{
  "question": "What are the working hours at HipLab?"
}
```

**Response:**
```json
{
  "answer": "Working hours are Monday to Friday, 8:30 AM to 5:30 PM, with lunch break from 12:00 PM to 1:00 PM."
}
```

#### 2. **Chat Stream Endpoint (Token-by-Token Streaming)**

```
POST /chat/stream
Content-Type: application/json

{
  "question": "What is HipLab's leave policy?"
}
```

**Response** (Server-Sent Events):
```
data: {"token":"Employees"}
data: {"token":" have"}
data: {"token":" 12"}
...
data: {"done":true}
```

#### 3. **File Upload Endpoint**

```
POST /upload/file
Content-Type: multipart/form-data

file: <binary-file>
```

**Response:**
```json
{
  "filename": "document.txt",
  "file_path": "/path/to/document.txt",
  "file_size": 1024,
  "message": "File 'document.txt' uploaded successfully"
}
```

Supported formats: `.txt`, `.pdf`, `.docx` (max 50MB)

#### 4. **List All Documents**

```
GET /upload/documents
```

**Response:**
```json
{
  "documents": [
    {
      "filename": "policy.txt",
      "file_size": 2048,
      "created_at": 1703498400.5,
      "modified_at": 1703498400.5
    },
    {
      "filename": "handbook.pdf",
      "file_size": 5120,
      "created_at": 1703498400.5,
      "modified_at": 1703498400.5
    }
  ]
}
```

#### 5. **Download Document**

```
GET /upload/documents/{filename}
```

**Response**: Binary file download

#### 6. **Delete Document**

```
DELETE /upload/documents/{filename}
```

**Response:**
```json
{
  "message": "Document 'filename.txt' deleted successfully",
  "filename": "filename.txt"
}
```

#### 7. **Health Check**

```
GET /health
```

### API Documentation

Interactive API documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🌐 Running the Web Project

The web frontend is a static HTML/CSS/JavaScript application that communicates with the FastAPI server.

### Quick Start

#### Option 1: Direct File Opening

```bash
# Navigate to the web folder
cd src/web

# Open index.html directly in your browser
# On macOS:
open index.html

# On Windows:
start index.html

# On Linux:
xdg-open index.html
```

#### Option 2: Python HTTP Server

```bash
# From project root
python -m http.server 8080 --directory src/web
```

Then open: http://localhost:8080

#### Option 3: VS Code Live Server Extension

1. Install VS Code extension "Live Server"
2. Right-click `src/web/index.html`
3. Select "Open with Live Server"

### Configuration

Before running the frontend, ensure the API URL is correctly configured in `src/web/app.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000';
```

**For production**, update this to your deployed API URL:

```javascript
const API_BASE_URL = 'https://api.example.com';
```

### Features

- **Real-time Chat Interface**: Displays messages with streaming tokens
- **Quick Questions**: Pre-configured questions about HipLab policies
- **Auto-scroll**: Automatically scrolls to latest messages
- **Error Handling**: Displays user-friendly error messages
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### Browser Compatibility

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+


## 🛠️ Development Workflow

### Useful Makefile Commands

Check `Makefile` for common development tasks:

```bash
make help        # Display available commands
make install     # Install dependencies
make dev         # Start development servers
make test        # Run test suite
make lint        # Check code quality
```

### Project Structure Tips

- **Add new graph nodes**: Create files in `src/agent/nodes/`
- **Update prompts**: Modify `src/agent/config/prompts.py`
- **Adjust LLM settings**: Edit `src/agent/config/settings.py`
- **Add new API routes**: Extend `src/api/routes.py`
- **Update frontend**: Modify files in `src/web/`

## 📚 Additional Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [LangSmith Setup Guide](./LANGSMITH_SETUP.md)
- [Code Review Guidelines](./CODE_REVIEW.md)

## 📝 License

This project is licensed under the terms specified in the [LICENSE](./LICENSE) file.

## 🤝 Contributing

For contribution guidelines, please see [CODE_REVIEW.md](./CODE_REVIEW.md).

---

**Last Updated**: December 25, 2025

For questions or issues, please open an issue in the repository or contact the development team.
