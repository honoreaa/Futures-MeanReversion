# Pairs Trading Strategy: ES=F and NQ=F Mean Reversion

This repository implements a quantitative trading strategy based on **pairs trading** and **mean reversion** principles. The strategy focuses on identifying cointegrated pairs of financial instruments, calculating their statistical spread, generating trading signals based on the spread's deviation from its mean (using Z-scores), and backtesting the performance.

The chosen instruments for this analysis are the E-mini S&P 500 Futures (`ES=F`) and E-mini NASDAQ 100 Futures (`NQ=F`), which are often good candidates for pairs trading due to their high correlation and underlying economic drivers.

## 1. Summary

This project outlines a pairs trading strategy using `ES=F` and `NQ=F` futures contracts. The core idea is to exploit the mean-reverting nature of their cointegrated spread. We identify the optimal hedge ratio (beta) between the two assets, compute a normalized Z-score of their spread, and generate long/short signals when the Z-score crosses predefined entry and exit thresholds. The strategy's performance is then evaluated through a backtest, calculating key metrics such as cumulative PnL, total return, annualized return, annualized volatility, and the Sharpe Ratio.

## 2. Equations and Mathematical Foundation

### 2.1. Cointegration and Hedge Ratio

Cointegration implies that while two or more time series may be non-stationary individually, a linear combination of them is stationary. For two assets, $Y$ and $X$, their cointegrating relationship can be found through an Ordinary Least Squares (OLS) regression:

$$Y_t = \alpha + \beta X_t + \epsilon_t$$

Where:
* $Y_t$ is the price of the dependent asset (`ES=F`) at time $t$.
* $X_t$ is the price of the independent asset (`NQ=F`) at time $t$.
* $\alpha$ is the intercept.
* $\beta$ is the **hedge ratio** (or cointegration coefficient), representing the long-term equilibrium relationship between $Y$ and $X$. This is the crucial value for forming the spread.
* $\epsilon_t$ is the residual term, which, if $Y$ and $X$ are cointegrated, should be a stationary series (i.e., it reverts to its mean).

The **spread** is then defined as the deviation from this equilibrium:

$$\text{Spread}_t = Y_t - \beta X_t$$

For a valid pairs trade, the residuals ($\epsilon_t$) or the spread ($\text{Spread}_t$) must be stationary. This is typically tested using the Augmented Dickey-Fuller (ADF) test. A low p-value (e.g., less than 0.05 or 0.06) from the ADF test on the residuals indicates stationarity, confirming cointegration.

### 2.2. Z-score Calculation

To standardize the spread and identify deviations from its historical mean, a rolling Z-score is calculated. The Z-score measures how many standard deviations the current spread is from its rolling mean:

$$
Z_t = \frac{S_t - \mu_t}{\sigma_t}
$$

Where:
* $\text{Spread}_t$ is the current value of the spread.
* $\mu_{\text{spread},t}$ is the rolling mean of the spread over a defined lookback window (e.g., 30 days).
* $\sigma_{\text{spread},t}$ is the rolling standard deviation of the spread over the same lookback window.

### 2.3. Sharpe Ratio

The Sharpe Ratio is a measure of risk-adjusted return, indicating the average return earned in excess of the risk-free rate per unit of volatility (total risk).

$$\text{Sharpe Ratio} = \frac{(R_p - R_f)}{\sigma_p}$$

Where:
* $R_p$ = Annualized Portfolio Return (as a percentage).
* $R_f$ = Annualized Risk-Free Rate (as a percentage).
* $\sigma_p$ = Annualized Standard Deviation of Portfolio Returns (as a percentage).

A higher Sharpe Ratio indicates a better risk-adjusted performance.

## 3. Strategy Logic

The strategy follows these steps:

1. **Data Acquisition and Preparation:**

   * Historical daily price data for `ES=F` and `NQ=F` is loaded and merged.

   * Data is cleaned, ensuring correct data types (numeric prices, datetime index) and handling missing values.

2. **Cointegration Analysis and Hedge Ratio Calculation:**

   * The Engle-Granger two-step method is used to test for cointegration:

     * **Step 1:** An OLS regression of `ES=F` on `NQ=F` is performed to estimate the hedge ratio ($\beta$) and obtain the residuals.

     * **Step 2:** An Augmented Dickey-Fuller (ADF) test is applied to the residuals. A low p-value confirms stationarity of the spread, indicating cointegration.

   * The calculated $\beta$ from the OLS regression is used as the hedge ratio for forming the spread.

3. **Spread and Z-score Calculation:**

   * The spread is calculated using the formula: $\text{Spread}_t = \text{ES=F}_t - \beta \cdot \text{NQ=F}_t$.

   * A rolling Z-score of this spread is computed over a specified lookback window (e.g., 30 days).

4. **Signal Generation:**

   * **Long Signal (Buy the Spread):** Generated when the Z-score falls below a negative entry threshold (e.g., -2.0). This indicates the spread is significantly undervalued and is expected to revert upwards.

   * **Short Signal (Sell the Spread):** Generated when the Z-score rises above a positive entry threshold (e.g., +2.0). This indicates the spread is significantly overvalued and is expected to revert downwards.

   * **Exit Signal (Flat Position):** Generated when the Z-score reverts towards zero and crosses a smaller exit threshold (e.g., $\pm 0.5$). This indicates the mean reversion has likely occurred, and the position should be closed.

   * Positions are lagged by one day to simulate realistic entry/exit points.

5. **Backtesting:**

   * The strategy is backtested using the generated signals and historical price data.

   * Daily PnL is calculated based on the change in the spread, the position size, and the direction of the trade.

   * Cumulative PnL is tracked over time, starting with an initial capital.

   * Key performance metrics such as total return, annualized return, annualized volatility, and Sharpe Ratio are computed.

## 4. Findings

### 4.1. Cointegration Analysis

* The ADF test on the residuals of the `ES=F` vs `NQ=F` regression typically yields a low p-value, confirming that the pair is indeed cointegrated over the analyzed period (2015-01-01 to 2024-12-31).

* The estimated **hedge ratio ($\beta$)** between `ES=F` and `NQ=F` was found to be approximately **0.2241**. This means for every one unit of `ES=F` traded, approximately 0.2241 units of `NQ=F` should be traded in the opposite direction to maintain a market-neutral spread.

### 4.2. Initial Bug Identification and Resolution

Initially, the backtest showed a flat cumulative PnL. This was identified as a critical bug stemming from the hardcoding of `beta = 1.0` during the signal generation phase. This meant the spread, Z-score, and consequently the trading signals were based on an incorrect statistical relationship. The fix involved:

* **Dynamically calculating the hedge ratio ($\beta$)** using OLS regression *before* computing the spread and Z-score.

* Ensuring this **calculated $\beta$ was consistently used** throughout both the signal generation and the PnL calculation in the backtest.

### 4.3. Strategy Performance (After Fixes)

After correcting the `beta` calculation and ensuring its consistent use, the strategy generated meaningful trades and produced a positive cumulative PnL.

Using the provided backtest results:

* **Total Return:** $\$391,567.74$

* **Annualized Return:** $\$86,254.43$

* **Annualized Volatility:** $\$48,860.08$

* **Initial Capital:** $\$100,000$ (assumed from `FILE 4`)

* **Annualized Portfolio Return (Percentage):** $\frac{\$86,254.43}{\$100,000} \approx 86.25\%$

* **Annualized Volatility (Percentage):** $\frac{\$48,860.08}{\$100,000} \approx 48.86\%$

* **Assumed Risk-Free Rate ($R_f$):** $4.5\%$ (0.045)

The calculated Sharpe Ratio is:

$$\text{Sharpe Ratio} = \frac{(0.8625443 - 0.045)}{0.4886008} \approx 1.67$$

A Sharpe Ratio of **1.67** is considered **good** for a trading strategy, indicating a solid return for the level of risk taken.

## 5. Conclusions and Future Improvements

The pairs trading strategy, once correctly implemented with the dynamically calculated hedge ratio, demonstrates a positive risk-adjusted return. The ability to identify and exploit the mean-reverting behavior of cointegrated assets is validated.

To further enhance the strategy's performance and potentially improve the Sharpe Ratio (aiming for $\ge 2.0$), consider the following improvements:

* **Parameter Optimization:** Systematically test different `entry_threshold`, `exit_threshold`, and `window` (for Z-score calculation) values to find the optimal combination that maximizes the Sharpe Ratio while maintaining robustness.

* **Dynamic Hedge Ratio:** Instead of a single static beta for the entire period, consider using a rolling hedge ratio that adapts to changing market conditions.

* **Risk Management:**

  * **Stop-Loss Orders:** Implement clear stop-loss rules to limit downside risk on trades where the spread continues to diverge against the position, indicating a breakdown in the cointegrating relationship.

  * **Position Sizing:** Explore dynamic position sizing based on portfolio volatility or market conditions.

* **Transaction Costs:** Incorporate realistic transaction costs (commissions, slippage) into the backtest to get a more accurate representation of net profitability.

* **Diversification:** Expand the strategy to identify and trade multiple cointegrated pairs across different sectors or asset classes to diversify risk and potentially increase overall returns.

* **Market Regime Filtering:** Add logic to avoid trading during periods of high market volatility or when the correlation between the pair breaks down, as mean-reversion strategies can struggle in trending markets.

* **Alternative Cointegration Tests:** Explore other cointegration tests (e.g., Johansen test) for multi-variate cointegration or robustness checks.

This project serves as a strong foundation for developing and refining quantitative mean-reversion strategies.
