# reads llm settings from env vars so we can swap models without touching code

import os

MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4.1-mini")
MODEL_TEMPERATURE: float = float(os.getenv("MODEL_TEMPERATURE", "0"))
