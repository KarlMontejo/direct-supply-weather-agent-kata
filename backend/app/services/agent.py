# manages conversation sessions and talks to the procurement agent.
# each session keeps its full message history in memory so the agent
# has context across turns. also pulls out which tools were called
# during each turn so the frontend can display them.

import uuid
from backend.app.agent.procurement_agent import create_procurement_agent

# build the agent once, reuse it for every request
_agent = create_procurement_agent()

# in-memory session store — maps session_id to list of langgraph messages.
# in a real app this would be a database or cache, but for a demo this works.
_sessions: dict[str, list] = {}


def chat(session_id: str | None, user_message: str) -> tuple[str, list, list[str]]:
    """
    handle a single chat turn.

    takes the session id (or None to start fresh) and the user's new message.
    returns a tuple of:
      - session_id (created if it was None)
      - full message history as a list of (role, content, tools_used) tuples
      - tools used in this specific turn
    """
    # create a new session if needed
    if not session_id or session_id not in _sessions:
        session_id = session_id or str(uuid.uuid4())
        _sessions[session_id] = []

    # get the existing langgraph messages for this session
    history = _sessions[session_id]

    # add the user's new message and invoke the agent
    history.append({"role": "user", "content": user_message})
    result = _agent.invoke({"messages": history})

    # langgraph returns the full message list including new tool calls
    # and the final assistant reply. replace our history with it.
    updated_messages = result["messages"]
    _sessions[session_id] = updated_messages

    # figure out which tools were called in this turn.
    # we scan backwards from the end to find tool_calls on AIMessages
    # that happened after the last user message we sent.
    tools_this_turn: list[str] = []
    for msg in reversed(updated_messages):
        # stop when we hit the user message we just sent
        if hasattr(msg, "content") and getattr(msg, "type", None) == "human":
            break
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                name = tc.get("name", "")
                if name and name not in tools_this_turn:
                    tools_this_turn.append(name)

    # reverse so tools appear in the order they were called
    tools_this_turn.reverse()

    # build a clean list of (role, content, tools_used) for the response.
    # we skip intermediate tool call / tool result messages — the frontend
    # only needs user messages and final assistant replies.
    clean_history: list[tuple[str, str, list[str]]] = []
    accumulated_tools: list[str] = []

    for msg in updated_messages:
        msg_type = getattr(msg, "type", None)

        if msg_type == "human":
            clean_history.append(("user", msg.content, []))
            accumulated_tools = []

        elif msg_type == "ai" and hasattr(msg, "tool_calls") and msg.tool_calls:
            # this is an intermediate message where the agent decides to call tools.
            # collect the tool names but don't add a message yet.
            for tc in msg.tool_calls:
                name = tc.get("name", "")
                if name and name not in accumulated_tools:
                    accumulated_tools.append(name)

        elif msg_type == "ai" and msg.content:
            # this is the agent's actual text reply to the user
            clean_history.append(("assistant", msg.content, list(accumulated_tools)))
            accumulated_tools = []

        # skip ToolMessage entries — they're internal plumbing

    return session_id, clean_history, tools_this_turn
