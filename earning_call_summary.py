from stock_agent_python.send_earning_call_summary_report import send_earning_call_summary_report
from stock_agent_python.constants import STOCK_SYMBOLS
from dotenv import load_dotenv
import os



load_dotenv()

RECIPIENT_EMAILS = os.getenv("RECIPIENT_EMAILS")

if __name__ == "__main__":
    send_earning_call_summary_report(RECIPIENT_EMAILS, STOCK_SYMBOLS)
