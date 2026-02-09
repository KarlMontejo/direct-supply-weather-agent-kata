# fastapi entrypoint — this is what uvicorn loads.
# sets up cors so the next.js frontend can call us, and mounts the chat route.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.chat import router as chat_router

app = FastAPI(
    title="Direct Supply Procurement Assistant",
    description="backend api for the procurement chatbot",
    version="0.1.0",
)

# let the next.js dev server talk to us
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
