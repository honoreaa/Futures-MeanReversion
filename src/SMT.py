def smt_divergence(y, x, lookback=20):
    highs_y = y.rolling(lookback).max()
    highs_x = x.rolling(lookback).max()
    divergence = (y >= highs_y) & (x < highs_x)
    return divergence.astype(int)
