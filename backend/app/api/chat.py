# the chat endpoint — receives a user message, runs it through the agent,
# and sends back the full conversation history with tool usage annotations.

from fastapi import APIRouter, HTTPException

from backend.app.schemas.request import ChatRequest
from backend.app.schemas.response import ChatResponse, MessageOut
from backend.app.services import agent as agent_service

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """
    send a message to the procurement agent.

    the backend keeps the conversation history — the frontend just sends
    the new message and a session_id. we return the full history so the
    frontend can render the whole chat including which tools were used.
    """
    try:
        session_id, history, _ = agent_service.chat(req.session_id, req.message)

        messages_out = [
            MessageOut(role=role, content=content, tools_used=tools)
            for role, content, tools in history
        ]

        return ChatResponse(session_id=session_id, messages=messages_out)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
