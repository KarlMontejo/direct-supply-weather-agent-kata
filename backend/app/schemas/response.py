# what we send back to the frontend — the full conversation so far,
# plus which tools the agent used to produce each assistant reply.

from pydantic import BaseModel


class MessageOut(BaseModel):
    role: str                       # "user" or "assistant"
    content: str
    tools_used: list[str] = []      # only populated for assistant messages


class ChatResponse(BaseModel):
    session_id: str
    messages: list[MessageOut]
