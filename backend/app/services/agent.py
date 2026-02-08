"""
Agent service — backend bridge to the AI orchestration layer.

Provides a simple interface for the backend API to invoke the
procurement agent without knowing its internal wiring.
"""

from ai_services.agent.procurement_agent import create_procurement_agent

# Create the agent once at import time so it's reused across requests.
_agent = create_procurement_agent()


def invoke(messages: dict) -> dict:
    """
    Invoke the procurement agent with a conversation history.

    Args:
        messages: A dict with a "messages" key containing a list of
                  message dicts (role + content), e.g.:
                  {
                      "messages": [
                          {"role": "user", "content": "I need bread for 50 meals"}
                      ]
                  }

    Returns:
        The updated messages dict including the agent's response
        and any intermediate tool calls.
    """
    return _agent.invoke(messages)
