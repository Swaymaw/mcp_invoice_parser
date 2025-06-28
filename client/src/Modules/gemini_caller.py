from functools import lru_cache
from google.genai import types
from google.genai.types import GenerateContentConfig, Content, Part
from src.Utils.prompts import SystemPrompts
from src.Modules.base_caller import BaseCaller
from google.genai import Client
from src.Utils.helper import getResponseString
import traceback
import os


class GeminiMCPClient(BaseCaller):
    def __init__(self):
        super().__init__()
        api_key = os.environ["GOOGLE_AI_API_KEY"]
        self.gemini_client = Client(api_key=api_key)
        self.messages = []

    @lru_cache()
    def format_tools(self):
        return [
            types.Tool(
                function_declarations=[
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": {
                            k: v
                            for k, v in tool.inputSchema.items()
                            if k not in ["additionalProperties", "$schema"]
                        },
                    },
                ]
            )
            for tool in self.tools
        ]

    async def reset(self):
        self.messages = []
        self.tool_calls = []
        await self._refresh_tools()

    async def ask_query(
        self, user_query: str, images: list[bytes] = []
    ) -> tuple[str, list[dict[str, str]]]:
        parts = []
        for image_bytes in images:
            parts.append(
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
            )

        parts.append(
            types.Part.from_text(text=user_query)
        )  # Convert text to Part

        # Append as ONE user message
        self.messages.append(Content(role="user", parts=parts))

        all_texts = []
        tool_calls = []

        while True:
            tool_call_present = False

            response = self.gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=self.messages,
                config=GenerateContentConfig(
                    candidate_count=1,
                    system_instruction=SystemPrompts.InvoiceManager,
                    tools=self.format_tools(),
                ),
            )

            resp_parts = response.candidates[0].content.parts

            if resp_parts:
                for part in resp_parts:
                    if part.function_call:
                        tool_call_present = True
                        name = part.function_call.name or ""
                        args = part.function_call.args

                        self.messages.append(
                            Content(role="model", parts=[part])
                        )

                        try:
                            resp = await self.session.call_tool(name, args)
                            resp_string = getResponseString(resp.content)
                        except McpError:
                            resp_string = traceback.format_exc()

                        tool_calls.append(
                            {
                                "name": name,
                                "args": args,
                                "result": resp_string,
                            }
                        )
                        self.messages.append(
                            Content(
                                role="model",
                                parts=[
                                    types.Part.from_function_response(
                                        name=name, response=resp_string
                                    ),
                                ],
                            )
                        )

                    if part.text:
                        all_texts.append(part.text)

            if not tool_call_present:
                break

        return "\n\n---\n\n".join(all_texts), tool_calls
