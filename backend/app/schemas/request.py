# what the frontend sends us — just a session id and the new message.
# the backend owns the full conversation history, the frontend doesn't
# need to track or send it back each time.

from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str | None = None   # omit to start a new conversation
    message: str                    # the user's latest message
