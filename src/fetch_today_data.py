'''
import yfinance as yf
import pandas as pd
import os

def fetch_today_market_data(stocks, output_path):
    """
    Fetch today's stock market data for NSE stocks.
    Invalid symbols are skipped with a warning.
    """

    all_data = []
    invalid_symbols = []

    for symbol in stocks:
        ticker = yf.Ticker(symbol + ".NS")
        hist = ticker.history(period="1y")


        if hist.empty:
            invalid_symbols.append(symbol)
            continue

        hist = hist.reset_index()
        hist["symbol"] = symbol
        all_data.append(hist)

    if not all_data:
        raise ValueError("No valid stock data fetched. Please check symbols.")

    df = pd.concat(all_data, ignore_index=True)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    if invalid_symbols:
        print("⚠️ Invalid / unavailable symbols skipped:", invalid_symbols)

    return df
'''

import yfinance as yf
import pandas as pd
import os

def fetch_today_market_data(symbols, save_path):

    # ensure directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # add .NS suffix safely
    symbols = [
        s if s.endswith(".NS") else s + ".NS"
        for s in symbols
    ]

    # download data (THIS METHOD WORKS ON STREAMLIT CLOUD)
    df = yf.download(
        tickers=symbols,
        period="1y",
        interval="1d",
        group_by="ticker",
        auto_adjust=True,
        threads=False
    )

    if df.empty:
        raise ValueError("No valid stock data fetched. Please check symbols.")

    # convert to proper format
    all_data = []

    for symbol in symbols:
        try:
            temp = df[symbol].copy()
            temp["Symbol"] = symbol
            temp.reset_index(inplace=True)
            all_data.append(temp)
        except:
            continue

    if not all_data:
        raise ValueError("No valid stock data fetched. Please check symbols.")

    final_df = pd.concat(all_data, ignore_index=True)

    final_df.to_csv(save_path, index=False)

    return final_df



