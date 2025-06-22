from mcp.server.fastmcp import FastMCP
from src.Modules.sheet_interface import add_rows, get_rows
import json

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

    update_information = add_rows(
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


# @mcp.tool()
# def save_item_wise_data_to_sheets(
#     InvoiceNo: int,
#     ItemDescription: str,
#     ItemQuantity: float,
#     UnitOfMeasure: str,
#     NetPrice: float,
#     NetWorth: float,
#     VATPercent: int,
#     GrossWorth: float,
# ):
#     """
#     This endpoint appends a row on google sheet based on item-wise data extracted from the current invoice information sent by the user.
#     InvoiceNo: int = Invoice number information extracted from the invoice image sent.
#     ItemDescription: str = Description for the specific item for which row is being updated in google sheets in the current calls.
#     ItemQuantity: int = Quantity for the specific item for which row is being updated in google sheets in the current calls.
#     UnitOfMeasure: str = UM (Unit of Measure) for the specific item for which row is being updated in google sheets in the current calls.
#     NetPrice: float = Net Price for the specific item for which row is being updated in google sheets in the current calls.
#     NetWorth: float = Net Worth for the specific item for which row is being updated in google sheets in the current calls.
#     VATPercent: float = VAT Percent truncated to an integer for the specific item for which row is being updated in google sheets in the current calls.
#     GrossWorth: float = Gross Worth for the specific item for which row is being updated in google sheets in the current calls.
#     """
#     update_information = add_row(
#         [
#             [
#                 InvoiceNo,
#                 ItemDescription,
#                 ItemQuantity,
#                 UnitOfMeasure,
#                 NetPrice,
#                 NetWorth,
#                 VATPercent,
#                 GrossWorth,
#             ]
#         ],
#         data_type="Item",
#     )

#     return update_information


@mcp.tool()
def save_item_wise_data_to_sheets(
    InvoiceNo: int,
    ItemDescription: list[str],
    ItemQuantity: list[float],
    UnitOfMeasure: list[str],
    NetPrice: list[float],
    NetWorth: list[float],
    VATPercent: list[int],
    GrossWorth: list[float],
):
    """
    This endpoint appends a row on google sheet based on item-wise data extracted from the current invoice information sent by the user.
    InvoiceNo: int = Invoice number information extracted from the invoice image sent.
    ItemDescription: list[str] = List of descriptions for the items corresponding to the invoice uploaded by user in respective order.
    ItemQuantity: list[int] = List of Quantities for the items corresponding to the invoice uploaded by user in respective order.
    UnitOfMeasure: list[str] = List of UM (Unit of Measure) for the items corresponding to the invoice uploaded by user in respective order.
    NetPrice: list[float] = List of Net Price for the items corresponding to the invoice uploaded by user in respective order.
    NetWorth: list[float] = List of Net Worth for the items corresponding to the invoice uploaded by user in respective order.
    VATPercent: list[float] = List of VAT percentage truncated to an integer for the items corresponding to the invoice uploaded by user in respective order.
    GrossWorth: list[float] = List of Gross Worth for the items corresponding to the invoice uploaded by user in respective order.
    """

    upload_data = []

    # validate the lengths:
    assert (
        len(ItemDescription)
        == len(ItemQuantity)
        == len(UnitOfMeasure)
        == len(NetPrice)
        == len(NetWorth)
        == len(VATPercent)
        == len(GrossWorth)
    ), "The lengths for all the attributes provided is unequal which means data is either missing or format is incorrect. Make sure length for all attributes which represent the number of items in a invoice are all equal. Please validate that row-wise data for each item is presented correctly in the lists without any missing value and in their correct order"

    for i in range(len(ItemDescription)):
        upload_data.append(
            [
                InvoiceNo,
                ItemDescription[i],
                ItemQuantity[i],
                UnitOfMeasure[i],
                NetPrice[i],
                NetWorth[i],
                VATPercent[i],
                GrossWorth[i],
            ]
        )
    update_information = add_rows(
        upload_data,
        data_type="Item",
    )

    return update_information


@mcp.tool()
def get_invoice_data_from_sheets_via_invoice_number(InvoiceNo: int) -> str:
    """
    InvoiceNo: int = Get invoice_metadata and item_data for Invoice number for which information is required to anwer user's queries.
    """

    invoice_metadata = get_rows(
        str(InvoiceNo), target_column=1, data_type="Invoice"
    )
    item_data = get_rows(str(InvoiceNo), target_column=0, data_type="Item")
    data = {"invoice_metadata": invoice_metadata, "item_data": item_data}

    return json.dumps(data)


if __name__ == "__main__":
    mcp.run(transport="stdio")
