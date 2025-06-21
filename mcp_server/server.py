from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("invoice_parser")


@mcp.tool()
def save_invoice_metadata_to_sheets():
    pass


@mcp.tool()
def save_item_wise_data_to_sheets():
    pass


@mcp.tool()
def get_invoice_data_from_sheets():
    pass
