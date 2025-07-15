import yfinance as yf
import pandas as pd
from pathlib import Path

def download_futures(symbol, start="2015-01-01", end="2024-12-31"):
    print(f"Downloading {symbol}...")
    df = yf.download(symbol, start=start, end=end, progress=False)
    if df.empty:
        raise ValueError(f"No data returned for {symbol}")
    df = df[['Close']].rename(columns={'Close': symbol})

    return df

def save_to_csv(df, symbol, data_dir="data"):
    Path(data_dir).mkdir(exist_ok=True)
    file_path = Path(data_dir) / f"{symbol}.csv"
    df.to_csv(file_path)
    print(f"Saved {symbol} data to {file_path}")

def load_and_merge(symbols, start, end):
    dfs = []
    for s in symbols:
        df = download_futures(s, start, end)
        dfs.append(df)
        save_to_csv(df, s)
    merged = pd.concat(dfs, axis=1).dropna()
    merged.index = pd.to_datetime(merged.index)
    merged = merged.sort_index()
    merged.to_csv("data/merged.csv")
    print("Merged dataset saved to data/merged.csv")
    return merged
