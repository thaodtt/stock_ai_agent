from yahoo_fin.stock_info import get_data
from loguru import logger
import pandas as pd

new_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def get_stock_price(symbol, start_date, end_date):
    data = get_data(symbol, start_date, end_date, headers=new_headers)
    df = data[["adjclose"]].rename(columns={"adjclose": "price"})
    df['date'] = pd.to_datetime(df.index).date
    df = df.sort_values(by='date').reset_index(drop=True)
    return df[['date', 'price']]
