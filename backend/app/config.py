"""
Application configuration.

Centralizes settings for the backend and AI services.
Values are read from environment variables with sensible defaults.
"""

import os

# LLM configuration
MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4.1-mini")
MODEL_TEMPERATURE: float = float(os.getenv("MODEL_TEMPERATURE", "0"))
