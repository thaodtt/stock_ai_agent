import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

SERVICE_ACCOUNT_FILE = '.google_sheet_api.json'
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly'
]

def read_google_sheets(spreadsheet_id, sheet_name="Sheet1"):
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.worksheet(sheet_name)
    records = worksheet.get_all_records()
    return pd.DataFrame(records)
