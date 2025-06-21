from random import getstate
from typing_extensions import Set
from src.Utils.helper import getSheetClient
from src.Utils.config import SheetConfig


def add_row(data: list[list[str | float | int]], data_type: str) -> str:
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
