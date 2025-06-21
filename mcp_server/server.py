from mcp.server.fastmcp import FastMCP
from src.Modules.sheet_uploader import add_row

# Initialize FastMCP server
mcp = FastMCP("invoice_parser")


@mcp.tool()
def save_invoice_metadata_to_sheets(
    Date: str,
    InvoiceNo: int,
    SellerInformation: str,
    ClientInformation: str,
    VATPercent: int,
    NetWorth: float,
    VAT: float,
    GrossWorth: float,
) -> str:
    """
    This endpoint appends a row on google sheet based data extracted from the current invoice information sent by the user.
    Date: str = The date of invoice in DD/MM/YYYY format
    InvoiceNo: int = Invoice number information extracted from the invoice image sent.
    SellerInformation: str = The seller address and name information provided in the invoice uploaded as a single string.
    ClientInformation: str = The client address and name information provided in the invoice uploaded as a single string.
    VATPercent: int = The summary vat information for the invoice truncated to an integer
    NetWorth: float = the summary net worth information in the invoice.
    VAT: float = calculated VAT gross based on net worth in the invoice summary section.
    GrossWorth: float = Net Woth + VAT for the invoice present in the bottom summary section.
    """

    update_information = add_row(
        [
            [
                Date,
                InvoiceNo,
                SellerInformation,
                ClientInformation,
                VATPercent,
                NetWorth,
                VAT,
                GrossWorth,
            ]
        ],
        data_type="Invoice",
    )

    return update_information


@mcp.tool()
def save_item_wise_data_to_sheets():
    pass


@mcp.tool()
def get_invoice_data_from_sheets():
    pass


if __name__ == "__main__":
    mcp.run(transport="stdio")
