import pandas as pd

def compute_spread(y, x, beta):
    return y - beta * x

def compute_zscore(spread, window=30):
    mean = spread.rolling(window).mean()
    std = spread.rolling(window).std()
    return (spread - mean) / std

def generate_signals(zscore, entry_threshold=2, exit_threshold=0.5):
    signals = pd.Series(0, index=zscore.index)
    signals[zscore > entry_threshold] = -1
    signals[zscore < -entry_threshold] = 1
    signals[abs(zscore) < exit_threshold] = 0
    return signals.ffill().fillna(0)