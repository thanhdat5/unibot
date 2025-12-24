from fastapi import FastAPI
from api.routes import router

def create_app() -> FastAPI:
    app = FastAPI(
        title="UniBot API",
        version="1.0.0",
        description="RAG chatbot API powered by LangGraph"
    )

    app.include_router(router)

    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    return app


app = create_app()
