from pydantic import BaseModel


class ChatResponse(BaseModel):
    """Outbound chat response to the frontend."""
    reply: str
