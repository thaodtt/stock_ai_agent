import requests
from dotenv import load_dotenv
import os
import pandas as pd
from io import StringIO
import datetime as dt

load_dotenv()
ALPHAVANTAGE_API = os.getenv("ALPHAVANTAGE_API")

def get_all_earnings_three_months():
    CSV_URL = f'https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month&apikey={ALPHAVANTAGE_API}'

    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
    df = pd.read_csv(StringIO(decoded_content))
    return df

def get_earning_dates(start_date: str, end_date: str, symbols: list[str])->dict[str, list[str]]:
    df = get_all_earnings_three_months()
    df['date'] = df['reportDate'].astype(str)
    filtered_df = df[df['symbol'].isin(symbols)&(df['date']>=start_date)&(df['date']<=end_date)]
    return {date: tt['symbol'].values.tolist() for date, tt in filtered_df.groupby('date')}

def get_next_week_earning_dates(symbols):
    today = dt.datetime.now().date()
    next_week = today + dt.timedelta(days=7)
    return get_earning_dates(today.strftime('%Y-%m-%d'), next_week.strftime('%Y-%m-%d'), symbols)
