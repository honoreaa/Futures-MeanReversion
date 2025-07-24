import pandas as pd

def compute_spread(y, x, beta):
    return y - beta * x

def compute_zscore(spread, window=30):
    mean = spread.rolling(window).mean()
    std = spread.rolling(window).std()
    zscore = (spread - mean) / std
    return zscore

def generate_signals(zscore, entry_threshold=3.0, exit_threshold=0.25):
    signals = pd.Series(0, index=zscore.index)
    signals[zscore > entry_threshold] = -1
    signals[zscore < -entry_threshold] = 1
    signals[abs(zscore) < exit_threshold] = 0
    return signals.ffill().fillna(0)