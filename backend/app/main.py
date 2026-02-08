"""
FastAPI application entrypoint.

Provides the backend API that the frontend calls. The backend
orchestrates requests — it validates input, invokes the AI agent,
and returns structured responses. It does not perform reasoning,
product selection, or substitution logic.
"""

from fastapi import FastAPI
from backend.app.services import agent as agent_service

app = FastAPI(
    title="Direct Supply Procurement Assistant",
    description="Backend API for the agentic food procurement chatbot.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    """Liveness probe."""
    return {"status": "ok"}
