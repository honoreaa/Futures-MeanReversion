# Mean Reversion - Analyzing the Efficiency of Pairs Trading with ES and NQ

My goal with this repo is to implement a quantitative trading strategy based on **pairs trading** and **mean reversion** principles, that focuses on identifying cointegrated pairs of financial instruments, calculating their statistical spread, generating trading signals based on the spread's deviation from its mean using Z-scores, and then backtesting the performance.
I chose E-mini S&P500 Futures (`ES=F`) and E-mini NASDAQ 100 Futures (`NQ=F`) as the two instruments that I predicted would be cointegrated. 

## 1. Strucute & Quick Overview

The main idea here is to exploit the mean-reverting nature of a cointegrated spread between NQ and ES. I will identify the optimal hedge ratio (beta) between the two assets, compute a normalized Z-score of their spread, and generate long/short signals when the Z-score crosses predefined entry and exit thresholds. Then, I'll evaluate the strategy's performance through backtasting and return cumulative PnL, total return, annualized return, annualized volatility, and the Sharpe Ratio.

## 2. Equations and Mathematical Foundation

### 2.1. Cointegration and Hedge Ratio

Cointegration implies that while two or more time series may be non-stationary individually, a linear combination of them IS stationary. For two assets, $Y$ and $X$, their cointegrating relationship can be found through an Ordinary Least Squares (OLS) regression:

$$Y_t = \alpha + \beta X_t + \epsilon_t$$

Where:
* $Y_t$ is the price of the dependent asset (`ES=F`) at time $t$.
* $X_t$ is the price of the independent asset (`NQ=F`) at time $t$.
* $\alpha$ is the intercept.
* $\beta$ is the **hedge ratio** (or cointegration coefficient), representing the long-term equilibrium relationship between $Y$ and $X$. This pretty much forms the spread.
* $\epsilon_t$ is the residual term, which, if $Y$ and $X$ are cointegrated, should be a stationary series, meaning it reverts to its mean.

The **spread** is then defined as the deviation from this state (which we will call an equilibrium):

$$\text{Spread}_t = Y_t - \beta X_t$$

For a valid pairs trade, the residuals ($\epsilon_t$) or the spread ($\text{Spread}_t$) must be stationary. This is typically tested using the Augmented Dickey-Fuller (ADF) test. A low p-value from the ADF test on the residuals indicates stationarity, confirming cointegration.

In my implementation, the ADF P-value was 0.039, which proves cointegration.

<img width="596" height="474" alt="Screenshot 2025-07-24 at 8 26 25 AM" src="https://github.com/user-attachments/assets/ef32af2d-2e6c-4e34-a3ab-268a40c39a41" />

### 2.2. Z-score Calculation

To standardize the spread and identify deviations from its historical mean, a rolling Z-score is calculated. The Z-score measures how many standard deviations the current spread is from its rolling mean:

$$
Z_t = \frac{S_t - \mu_t}{\sigma_t}
$$

Where:
* $\text{Spread}_t$ is the current value of the spread.
* $\mu_{\text{spread},t}$ is the rolling mean of the spread over a defined lookback window (I set to 30 days).
* $\sigma_{\text{spread},t}$ is the rolling standard deviation of the spread over the same lookback window.

### 2.3. Sharpe Ratio

The Sharpe Ratio is a measure of risk-adjusted return, indicating the average return earned in excess of the risk-free rate per unit of volatility (total risk).

$$\text{Sharpe Ratio} = \frac{(R_p - R_f)}{\sigma_p}$$

Where:
* $R_p$ = Percent Annualized Portfolio Return.
* $R_f$ = Percent Annualized Risk-Free Rate.
* $\sigma_p$ = Percent Annualized Standard Deviation of Portfolio Returns.

A higher Sharpe Ratio generally indicates a better risk-adjusted performance.

In my case, the Sharpe Ratio was 1.67, which is generally considered above average.

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

4. **Signal Generation:**

   * **Long Signal (Buy the Spread):** Generated when the Z-score falls below a negative entry threshold. This indicates the spread is significantly undervalued and is expected to revert upwards.

   * **Short Signal (Sell the Spread):** Generated when the Z-score rises above a positive entry threshold. This indicates the spread is significantly overvalued and is expected to revert downwards.

   * **Exit Signal (Flat Position):** Generated when the Z-score reverts towards zero and crosses a smaller exit threshold. This indicates the mean reversion has likely occurred, and the position should be closed.

   * Positions are lagged by one day to simulate realistic entry/exit points.
<img width="1139" height="547" alt="Screenshot 2025-07-24 at 8 31 45 AM" src="https://github.com/user-attachments/assets/d6b5c534-f6f8-4b67-999e-9ceb86b459a7" />

5. **Backtesting:**

   * The strategy is backtested using the generated signals and historical price data.

   * Daily PnL is calculated based on the change in the spread, the position size, and the direction of the trade.

   * Cumulative PnL is tracked over time, starting with an initial capital.

   * Key performance metrics such as total return, annualized return, annualized volatility, and Sharpe Ratio are computed.

## 4. Findings

### 4.1. Cointegration Analysis

* The ADF test on the residuals of the `ES=F` vs `NQ=F` regression typically yields a low p-value, confirming that the pair is indeed cointegrated over the analyzed period (2021-01-01 to 2025-07-22).

* The estimated **hedge ratio ($\beta$)** between `ES=F` and `NQ=F` was found to be approximately **0.2241**. This means for every one unit of `ES=F` traded, approximately 0.2241 units of `NQ=F` should be traded in the opposite direction to maintain a market-neutral spread.


### 4.2. Strategy Performance

<img width="1143" height="550" alt="Screenshot 2025-07-24 at 8 32 45 AM" src="https://github.com/user-attachments/assets/228edc92-3c12-42e8-8f45-2372d123266a" />

Using the provided backtest results:

* **Total Return:** $\$391,567.74$

* **Annualized Return:** $\$86,254.43$

* **Annualized Volatility:** $\$48,860.08$

* **Initial Capital:** $\$100,000$

* **Annualized Portfolio Return (Percentage):** $\frac{\$86,254.43}{\$100,000} \approx 86.25\%$

* **Annualized Volatility (Percentage):** $\frac{\$48,860.08}{\$100,000} \approx 48.86\%$


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

* **Alternative Cointegration Tests:** Explore other cointegration tests for multi-variate cointegration or robustness checks.

I had a blast with this project! Shoot me an email at haalexander@ucdavis.edu if you'd like to learn more or collaborate!
