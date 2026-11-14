"""FastAPI application entrypoint for Smart Email Manager."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import email_router


def create_app() -> FastAPI:
    """Construct and configure the FastAPI application."""
    application = FastAPI(
        title="Smart Email Manager API",
        description="AGY-container-powered smart email analysis, cleanup, and topic clustering service.",
        version="0.1.0",
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(email_router)
    return application


app = create_app()
