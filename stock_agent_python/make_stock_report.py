import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from .get_stock_price import get_stock_price
from loguru import logger

def make_stock_report(stock_symbols, moving_average_ranges, price_col='price'):
    results = []
    today = datetime.now().date() # Get today's date
    max_ma_range = 7/5* max(moving_average_ranges) if moving_average_ranges else 0
    start_of_year = datetime(today.year, 1, 1).date()
    earliest_date_needed_for_ma = today - timedelta(days=max_ma_range + 30) # Add buffer

    fetch_start_date = min(start_of_year, earliest_date_needed_for_ma).strftime('%Y-%m-%d')
    fetch_end_date = today.strftime('%Y-%m-%d')

    for symbol in stock_symbols:
        logger.info(f"Fetching data for {symbol} from {fetch_start_date} to {fetch_end_date}...")
        try:
            # Fetch historical data for the required period
            df = get_stock_price(symbol, fetch_start_date, fetch_end_date)

            if df.empty:
                logger.warning(f"No data available for {symbol}. Skipping.")
                continue

            current_price = df.iloc[-1][price_col]
            stock_info = {'Symbol': symbol, 'Latest date': df.date.iloc[-1], 'Current Price': current_price}

            # Calculate Returns
            # 1 Week Return
            date_1_week_ago = today - timedelta(weeks=1)
            price_1_week_ago_series = df[df['date'] <= date_1_week_ago][price_col]
            if not price_1_week_ago_series.empty:
                price_1_week_ago = price_1_week_ago_series.iloc[-1]
                stock_info['1 Week Return (%)'] = ((current_price - price_1_week_ago) / price_1_week_ago) * 100
            else:
                stock_info['1 Week Return (%)'] = np.nan

            # 1 Month Return
            date_1_month_ago = today - timedelta(days=30) # Approximate 1 month
            price_1_month_ago_series = df[df['date'] <= date_1_month_ago][price_col]
            if not price_1_month_ago_series.empty:
                price_1_month_ago = price_1_month_ago_series.iloc[-1]
                stock_info['1 Month Return (%)'] = ((current_price - price_1_month_ago) / price_1_month_ago) * 100
            else:
                stock_info['1 Month Return (%)'] = np.nan

            # Year To Date (YTD) Return
            start_of_year_price_series = df[df['date'] >= start_of_year][price_col]
            if not start_of_year_price_series.empty:
                # Find the first price on or after the start of the year
                ytd_start_price_candidates = df[df['date'] >= start_of_year]
                if not ytd_start_price_candidates.empty:
                    ytd_start_price = ytd_start_price_candidates.iloc[0][price_col]
                    stock_info['YTD Return (%)'] = ((current_price - ytd_start_price) / ytd_start_price) * 100
                else:
                    stock_info['YTD Return (%)'] = np.nan
            else:
                stock_info['YTD Return (%)'] = np.nan


            # Calculate Moving Averages
            for ma_range in moving_average_ranges:
                # Ensure enough data points for the moving average
                if len(df) >= ma_range:
                    df[f'MA_{ma_range}'] = df['price'].rolling(window=ma_range).mean()
                    ma_price = df[f'MA_{ma_range}'].iloc[-1]
                    ma_pct = ((current_price - ma_price) / current_price) * 100 if current_price !=0 else np.nan
                    stock_info[f'{ma_range} MA'] = f'{ma_price:.2f} ({ma_pct:.2f}%)'
                else:
                    stock_info[f'{ma_range} MA'] = np.nan
                    logger.warning(f"Not enough data for {symbol} to calculate {ma_range}-day MA.")
            results.append(stock_info)

        except Exception as e:
            logger.exception(f"An error occurred while processing {symbol}: {e}")
            error_info = {'Symbol': symbol, 'Current Price': 'Error'}
            for col in ['1 Week Return (%)', '1 Month Return (%)', 'YTD Return (%)'] + \
                       [f'MA_{r}_Price' for r in moving_average_ranges] + \
                       [f'MA_{r}_Pct_From_Current' for r in moving_average_ranges]:
                error_info[col] = 'Error'
    df = pd.DataFrame(results)
    return df
