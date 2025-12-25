from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router, router_upload

def create_app() -> FastAPI:
    app = FastAPI(
        title="UniBot API",
        version="1.0.0",
        description="RAG chatbot API powered by LangGraph"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins, or specify: ["http://localhost:8080", "http://localhost:3000"]
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods including OPTIONS
        allow_headers=["*"],
    )

    app.include_router(router)
    app.include_router(router_upload)

    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    return app


app = create_app()
