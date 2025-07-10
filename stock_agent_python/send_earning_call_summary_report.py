import datetime as dt
from .send_email import send_email
from .earning_call_transcript import get_earning_call_summary
from .earning_dates import get_earning_dates
from loguru import logger

def get_quarter_from_date(date):
    year, month, _ = date.split('-')
    month = int(month)
    if month<=3:
        quarter = 4
    elif month>9:
        quarter = 3
    elif (month>3)&(month<=6):
        quarter = 1
    else:
        quarter = 2
    return f'{year}Q{quarter}'

def send_earning_call_summary_report(recipient_emails, symbols):
    today = dt.datetime.now().date().strftime('%Y-%m-%d')
    earning_by_date = get_earning_dates(today, today, symbols)
    logger.info(earning_by_date)
    earning_today = earning_by_date.get(today, [])
    if not earning_today:
        logger.info("No earning today, skip!")
        return
    logger.info(f"THere are {len(earning_today)} companies with earning today: {earning_today}")
    quarter = get_quarter_from_date(today)
    summary_content = ""
    for symbol in earning_today:
        earning_summary = get_earning_call_summary(symbol=symbol, quarter=quarter)
        if isinstance(earning_summary, dict):
            earning_content = ""
            for key, value in earning_summary.items():
                earning_content += f"<h3>{key}</h3> <p>{value}</p>"
        else:
            earning_content = f'<p>{earning_summary}</p>'
        summary_content += f"<h2> Earning call summary for {symbol} {quarter}</h2> {earning_content}"
    html_body = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 800px; margin: auto; background: #f9f9f9; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
            h2 {{ color: #0056b3; border-bottom: 2px solid #eee; padding-bottom: 5px; margin-top: 20px; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .table-striped tbody tr:nth-child(odd) {{ background-color: #f9f9f9; }}
            .error-cell {{ background-color: #fdd; color: #a00; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
        {summary_content}
        </div>
    </body>
    </html>
    """
    subject = f"Earning call summary {today}"
    send_email(recipient_emails=recipient_emails, subject=subject, html_body=html_body)
