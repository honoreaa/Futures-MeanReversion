from src.load_data import load_and_merge
from src.cointegration import find_cointegrated_pairs
from src.signal_logic import compute_spread, compute_zscore

import pandas as pd
import matplotlib.pyplot as plt

symbols = ["ES=F", "NQ=F", "YM=F"]
data = load_and_merge(symbols, "2015-01-01", "2024-12-31")
print(data.head())



df = pd.read_csv("data/merged.csv", index_col=0, parse_dates=True)
pairs, summary = find_cointegrated_pairs(df)
summary.to_csv("outputs/cointegration_results.csv", index=False)
print(summary)

#initialize pairs
y = df["ES=F"]
x = df["NQ=F"]
beta = pairs[0][2]
spread = compute_spread(y, x, beta)
zscore = compute_zscore(spread)

z_df = pd.DataFrame({"Spread": spread, "Z-Score": zscore})
z_df.to_csv("outputs/zscore.csv")



# Cumulative PnL
# cumulative_pnl = pnl_series.cumsum()
# cumulative_pnl.plot(title="Cumulative PnL")
plt.savefig("outputs/cumulative_pnl.png")

# Z-Score Plot
plt.figure(figsize=(12,6))
plt.plot(zscore, label="Z-Score")
plt.axhline(2, color='r', linestyle='--')
plt.axhline(-2, color='r', linestyle='--')
plt.axhline(0, color='k')
plt.legend()
plt.title("Z-Score of Spread")
plt.savefig("outputs/zscore_plot.png")
