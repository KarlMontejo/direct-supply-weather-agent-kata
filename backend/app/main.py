"""
FastAPI application entrypoint.

Provides the backend API that the frontend calls. The backend
orchestrates requests — it validates input, invokes the AI agent,
and returns structured responses. It does not perform reasoning,
product selection, or substitution logic.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.chat import router as chat_router

app = FastAPI(
    title="Direct Supply Procurement Assistant",
    description="Backend API for the agentic food procurement chatbot.",
    version="0.1.0",
)

# CORS — allow the Next.js dev server to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)


@app.get("/health")
def health_check():
    """Liveness probe."""
    return {"status": "ok"}
