from mcp.types import Content, TextContent


def getResponseString(contents: list[Content]):
    final_resp = {}

    for content in contents:
        if isinstance(content, TextContent):
            final_resp["result"] = content.text

    return final_resp
