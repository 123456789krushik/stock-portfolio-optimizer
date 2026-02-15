import pandas as pd
import os

def load_and_clean_data(data_folder):
    """
    Load and combine NSE stock CSV files.
    Works for:
    1. Multiple CSV files (one per stock)
    2. Single combined CSV file (with symbol column)
    """

    if not os.path.exists(data_folder):
        raise FileNotFoundError(f"Folder not found: {data_folder}")

    all_files = [
        f for f in os.listdir(data_folder)
        if f.endswith(".csv") and f != "stock_metadata.csv"
    ]

    if not all_files:
        raise ValueError("No stock CSV files found in folder")

    df_list = []

    for file in all_files:
        file_path = os.path.join(data_folder, file)
        temp_df = pd.read_csv(file_path)

        # Normalize column names
        temp_df.columns = temp_df.columns.str.lower().str.strip()

        # Only create symbol column IF it doesn't already exist
        if "symbol" not in temp_df.columns:
            temp_df["symbol"] = file.replace(".csv", "")

        df_list.append(temp_df)

    df = pd.concat(df_list, ignore_index=True)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

    df.dropna(inplace=True)

    return df


def pivot_close_prices(df, selected_stocks=None):
    if selected_stocks is not None:
        df = df[df["symbol"].isin(selected_stocks)]

    return df.pivot(index="date", columns="symbol", values="close")
