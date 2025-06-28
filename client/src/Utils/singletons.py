from src.Modules.gemini_caller import GeminiMCPClient
from functools import lru_cache


@lru_cache(maxsize=1)
def getGeminiMCPClient() -> GeminiMCPClient:
    return GeminiMCPClient()
