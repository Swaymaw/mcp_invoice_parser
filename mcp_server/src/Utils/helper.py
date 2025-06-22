from googleapiclient.discovery import build
from google.oauth2 import service_account
from src.Utils.config import SheetConfig
from functools import lru_cache


@lru_cache(maxsize=1)  # Singleton Python
def getSheetClient():
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    creds = None
    creds = service_account.Credentials.from_service_account_file(
        SheetConfig.SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    return sheet


def get_column_name_from_index(col_number: int) -> str:
    """
    Converts the given index number to google sheet query friendly column name
    col_number: int = 0-indexed number for any column.
    """
    alphabets = "abcdefghijklmnopqrstuvwxyz"

    max_iter = 1

    while 26**max_iter <= col_number:
        max_iter += 1

    col_name = []
    for i in range(1, max_iter + 1):
        col_name.append(alphabets[col_number % 26])
        col_number //= 26
        col_number -= 1

    return "".join(col_name[::-1])
