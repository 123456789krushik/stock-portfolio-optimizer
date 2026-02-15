
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

def fetch_today_market_data(symbols, save_path):
    data = []

    for symbol in symbols:
        # add .NS if not present
        if not symbol.endswith(".NS"):
            symbol = symbol + ".NS"

        stock = yf.Ticker(symbol)
        hist = stock.history(period="1d")

        if not hist.empty:
            price = hist["Close"].iloc[-1]
            data.append({
                "Symbol": symbol,
                "Close": price
            })

    if not data:
        raise ValueError("No valid stock data fetched. Please check symbols.")

    df = pd.DataFrame(data)
    df.to_csv(save_path, index=False)

    return df
