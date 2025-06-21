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
