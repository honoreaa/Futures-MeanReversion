import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, coint
import pandas as pd

def adf_test(series):
    result = adfuller(series, autolag='AIC')
    return {
        "adf_stat": result[0],
        "p_value": result[1],
        "critical_values": result[4]
    }

def engle_granger_test(y, x):
    coint_t, p_value, _ = coint(y, x)
    return p_value

def estimate_hedge_ratio(y, x):
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    beta = model.params[1]
    return beta

def find_cointegrated_pairs(df, threshold=0.05):
    pairs = []
    results = []
    symbols = df.columns
    for i in range(len(symbols)):
        for j in range(i+1, len(symbols)):
            y = df[symbols[i]]
            x = df[symbols[j]]
            p = engle_granger_test(y, x)
            if p < threshold:
                beta = estimate_hedge_ratio(y, x)
                pairs.append((symbols[i], symbols[j], beta, p))
                results.append({
                    "pair": f"{symbols[i]} & {symbols[j]}",
                    "p_value": p,
                    "beta": beta
                })
    return pairs, pd.DataFrame(results)
