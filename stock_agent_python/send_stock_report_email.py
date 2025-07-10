import datetime
from .send_email import send_email
from .make_stock_report import make_stock_report
from .earning_dates import get_next_week_earning_dates
from premailer import transform


def send_stock_report_email(recipient_emails, stock_symbols, moving_average_ranges):
    stock_report_df = make_stock_report(stock_symbols, moving_average_ranges)
    stock_report_df = stock_report_df.sort_values('1 Week Return (%)', ascending=False).reset_index(drop=True)
    today = datetime.datetime.now()
    earning_by_date = get_next_week_earning_dates(stock_symbols)
    subject = f"Daily Stock Analysis Report - {today.strftime('%Y-%m-%d')}"

    # Convert DataFrame to HTML
    return_cols = ['1 Week Return (%)', '1 Month Return (%)', 'YTD Return (%)']
    html_table = stock_report_df.style.background_gradient(
        cmap='RdYlGn',
        subset=return_cols, # Apply gradient only to this column
        vmin=-20,
        vmax=20
    ).format(
        {col: '{:.2f}' for col in return_cols+['Current Price']}
    ).to_html(
        classes='table table-striped',
        index=False,
        float_format='%.2f'
    )

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
            <h2> Earning Schedule </h2>
            {earning_by_date}
            <h2>Daily Stock Analysis Report</h2>
            <p>Report generated at: {today.strftime('%Y-%m-%d %H:%M:%S')}</p>

            {html_table}

            <p>This report includes current prices, returns, and moving averages for the selected stocks.</p>
            <p>Best regards,</p>
            <p>Your Stock Analyst Bot</p>
        </div>
    </body>
    </html>
    """
    html_body = transform(html_body)
    send_email(recipient_emails=recipient_emails, subject=subject, html_body=html_body)
