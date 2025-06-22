from src.Utils.config import SheetConfig
from src.Utils.helper import getSheetClient, get_column_name_from_index


def add_rows(data: list[list[str | float | int]], data_type: str) -> str:
    sheet = getSheetClient()

    request = (
        sheet.values()
        .append(
            spreadsheetId=SheetConfig.SPREADSHEET_ID,
            range=SheetConfig.worksheet_name[data_type],
            valueInputOption="USER_ENTERED",
            body={"values": data},
        )
        .execute()
    )

    return f"Updated {request["updates"]['updatedRows']} number of rows in range {request["updates"]["updatedRange"]}"


def get_rows(
    target_value: str, target_column: int, data_type: str
) -> list[dict[str, str]]:
    sheet = getSheetClient()
    colName = get_column_name_from_index(target_column).upper()

    # First, get just the target column to find matching row numbers
    target_column_range = (
        f"{SheetConfig.worksheet_name[data_type]}!{colName}:{colName}"
    )

    result = (
        sheet.values()
        .get(
            spreadsheetId=SheetConfig.SPREADSHEET_ID, range=target_column_range
        )
        .execute()
    )

    target_column_values = result.get("values", [])
    print(target_column_values)

    # Find row numbers that match
    matching_row_numbers = []
    for i, row in enumerate(target_column_values):
        if row and row[0] == target_value:
            matching_row_numbers.append(
                i + 1
            )  # +1 because sheets are 1-indexed

    header = (
        (
            sheet.values()
            .batchGet(
                spreadsheetId=SheetConfig.SPREADSHEET_ID,
                ranges=f"{SheetConfig.worksheet_name[data_type]}!1:1",
            )
            .execute()
        )
        .get("valueRanges", [])[0]
        .get("values")[0]
    )

    # Now get the full rows for matching row numbers
    ranges = [
        f"{SheetConfig.worksheet_name[data_type]}!{row_num}:{row_num}"
        for row_num in matching_row_numbers
    ]

    matching_rows = []

    if ranges:
        result = (
            sheet.values()
            .batchGet(spreadsheetId=SheetConfig.SPREADSHEET_ID, ranges=ranges)
            .execute()
        )

        for value_range in result.get("valueRanges", []):
            if value_range.get("values"):
                values = value_range.get("values")[0]
                sample = {}
                for key, value in zip(header, values):
                    sample[key] = value

                matching_rows.append(sample)

    return matching_rows
