"""
POST /chat — accepts a conversation history and returns the agent's reply.
"""

from fastapi import APIRouter, HTTPException

from backend.app.schemas.request import ChatRequest
from backend.app.schemas.response import ChatResponse
from backend.app.services import agent as agent_service

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """
    Send a conversation to the procurement agent and get a reply.

    The frontend sends the full message history so the agent has
    context across turns. The backend extracts the final assistant
    message and returns it as a plain string.
    """
    try:
        payload = {
            "messages": [
                {"role": m.role, "content": m.content}
                for m in req.messages
            ]
        }
        result = agent_service.invoke(payload)

        # The agent returns a dict with a "messages" key.
        # The last message is the assistant's reply.
        last_msg = result["messages"][-1]
        reply = last_msg.content if hasattr(last_msg, "content") else str(last_msg)

        return ChatResponse(reply=reply)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
