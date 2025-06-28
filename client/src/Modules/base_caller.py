# %%
from httpx import stream
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamablehttp_client
from mcp import StdioServerParameters
from src.Utils.config import MCPServer
from urllib.parse import urlparse
from contextlib import AsyncExitStack


class BaseCaller:
    def __init__(self):
        self.stack = AsyncExitStack()
        self.tools = []

    async def connect(self):
        parsed = urlparse(MCPServer.server_path)
        if parsed.scheme not in ["http", "https"]:
            server_param = StdioServerParameters(
                command="uv",
                args=[
                    "--directory",
                    MCPServer.server_path,
                    "run",
                    "python",
                    "-W",
                    "ignore",
                    "server.py",
                ],
                cwd=MCPServer.server_path,
            )
            read, write = await self.stack.enter_async_context(
                stdio_client(server_param)
            )
            self.session = await self.stack.enter_async_context(
                ClientSession(read, write)
            )
        else:
            read, write, _ = await self.stack.enter_async_context(
                streamablehttp_client(MCPServer.server_path)
            )
            self.session = await self.stack.enter_async_context(
                ClientSession(read, write)
            )

        await self.session.initialize()
        await self._refresh_tools()

    async def _refresh_tools(self):
        res = await self.session.list_tools()
        self.tools = res.tools
