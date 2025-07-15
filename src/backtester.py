import pandas as pd

def backtest(y, x, beta, signals, cost=0.0001):
    pnl = []
    position = 0
    for i in range(1, len(signals)):
        prev_pos = position
        position = signals.iloc[i]
        ret = 0
        if prev_pos != 0:
            dy = y.iloc[i] - y.iloc[i - 1]
            dx = x.iloc[i] - x.iloc[i - 1]
            spread_change = dy - beta * dx
            ret = prev_pos * spread_change - 2 * cost * abs(prev_pos)
        pnl.append(ret)
    pnl_series = pd.Series(pnl, index=signals.index[1:])
    return pnl_series
