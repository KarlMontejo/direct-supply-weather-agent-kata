# simple arithmetic tool the agent uses for cost totals, quantity math, etc.

from langchain.tools import tool


@tool
def calculator(expression: str) -> str:
    """
    Evaluate a basic arithmetic expression and return the result as a string.

    Supports addition, subtraction, multiplication, division, and parentheses.

    Example inputs:
    - "2 + 2"
    - "10 / 5"
    - "(3 * 4) - 5"
    - "18.99 * 30"
    """
    try:
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"
