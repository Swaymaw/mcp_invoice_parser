from posix import stat
from robyn import Robyn
from robyn.robyn import Request, Response
from src.Utils.singletons import getGeminiMCPClient
from lifetime import startup_events, shutdown_events
from urllib.parse import unquote_plus
import json


def create_app() -> Robyn:
    app = Robyn(__file__)
    app.startup_handler(startup_events)
    app.shutdown_handler(shutdown_events)

    @app.get("/")
    async def index():
        return {"Service": "Alive"}

    @app.post("/ask")
    async def ask(request: Request):
        files = request.files or {}
        query_params = request.query_params

        user_query = unquote_plus(query_params.get("user_query", ""))

        if user_query.strip() == "":
            return {"content": "empty queries are not allowed"}

        list_binaries = list(files.values())

        client = getGeminiMCPClient()

        print(type(list_binaries[0]))

        ans, tool_calls = await client.ask_query(
            user_query, images=list_binaries
        )

        return {"response": ans, "tools_called": json.dumps(tool_calls)}

    return app


if __name__ == "__main__":
    app = create_app()
    app.start(port=8080, host="0.0.0.0")
