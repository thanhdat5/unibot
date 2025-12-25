from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from api.routes import router, router_upload


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses"""
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        # Set Referrer-Policy header
        response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response


def create_app() -> FastAPI:
    app = FastAPI(
        title="UniBot API",
        version="1.0.0",
        description="RAG chatbot API powered by LangGraph"
    )

    # Add security headers middleware
    app.add_middleware(SecurityHeadersMiddleware)

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods including OPTIONS, GET, POST, DELETE
        allow_headers=["*"],
        expose_headers=["*"],
    )

    app.include_router(router)
    app.include_router(router_upload)

    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    return app


app = create_app()
