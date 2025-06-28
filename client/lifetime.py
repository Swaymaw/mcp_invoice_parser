from src.Utils.singletons import getGeminiMCPClient


async def startup_events():
    print("Connecting to Gemini MCP Client")
    getGeminiMCPClient()
    print("✅ Client Instantiated Successfully")


async def shutdown_events():
    await getGeminiMCPClient().reset()
