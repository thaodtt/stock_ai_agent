from stock_agent_python.send_stock_report_email import send_stock_report_email
from stock_agent_python.read_google_sheet import read_google_sheets
from stock_agent_python.constants import MOVING_AVERAGE_RANGES, STOCK_SYMBOLS
from dotenv import load_dotenv
import os

load_dotenv()

RECIPIENT_EMAILS = os.getenv("RECIPIENT_EMAILS")
STOCK_NAME_SPREADSHEET_ID = os.getenv("STOCK_NAME_SPREADSHEET_ID", None)

if __name__ == "__main__":
    if not STOCK_NAME_SPREADSHEET_ID:
        stock_names = STOCK_SYMBOLS
    else:
        stock_name_df = read_google_sheets(spreadsheet_id=STOCK_NAME_SPREADSHEET_ID)
        stock_names = stock_name_df["name"].values
    send_stock_report_email(RECIPIENT_EMAILS, stock_names, MOVING_AVERAGE_RANGES)
