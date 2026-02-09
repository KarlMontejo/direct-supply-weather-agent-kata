from pydantic import BaseModel


class MessagePayload(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    """Inbound chat request from the frontend."""
    messages: list[MessagePayload]
