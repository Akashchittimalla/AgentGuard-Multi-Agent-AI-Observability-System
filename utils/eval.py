import re

def deterministic_guard(text: str):
    """Checks for specific forbidden patterns before the LLM even sees it."""
    forbidden_keywords = ["password", "secret_key", "internal_admin"]
    for word in forbidden_keywords:
        if word in text.lower():
            return True # Risk detected
    return False