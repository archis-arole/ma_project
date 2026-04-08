import numpy as np
import utils
import pandas as pd


def model(params, prices):
    '''
    This is the moving average model.
    sp is short period of moving average.
    lp is long period of moving average.
    Also expects long/short ratio.
    Note that this function is vectorized.
    '''
    returns = prices.pct_change()
    sp, lp, long_short_ratio = params
    # For now I don't want to introduce leverage
    long_short_ratio = 1
    ma_short = prices.rolling(sp).mean().shift(1)[lp + 1:]
    ma_long = prices.rolling(lp).mean().shift(1)[lp + 1:]
    signal = ma_long < ma_short
    trade = signal.ne(signal.shift(1))
    trade.iloc[0] = True
    returns_aligned = returns.reindex(signal.index).dropna()
    signal_aligned = signal.loc[returns_aligned.index]
    model_returns = returns_aligned * np.where(
        signal_aligned, long_short_ratio, -1
    )
    equity_curve = (1 + model_returns).cumprod()
    return equity_curve, model_returns


def model_stats(params, prices):
    equity_curve, model_returns = model(params, prices)
    equity = equity_curve.iloc[-1]
    mean_returns = model_returns.mean()
    std_returns = model_returns.std(ddof=1)
    sharpe_ratio = mean_returns / std_returns * np.sqrt(252)
    years = len(equity_curve) / 252
    CAGR = equity ** (1 / years) - 1
    running_max = equity_curve.cummax()
    drawdown = equity_curve / running_max - 1
    max_drawdown = drawdown.min()
    metrics = [
        "Mean Return",
        "Volatility",
        "Sharpe",
        "CAGR",
        "Max Drawdown",
        "Equity",
    ]
    values = [
        mean_returns,
        std_returns,
        sharpe_ratio,
        CAGR,
        max_drawdown,
        equity,
    ]
    metrics_df = pd.DataFrame(
        {"metrics": metrics, "value": values}
    )
    return metrics_df


raw_data = pd.read_csv('./nifty50_daily_last_year.csv')
data = raw_data.copy()
prices = data['Close']
print(model_stats([7, 21, 1], prices))
utils.plot_equity_curve(model([7, 21, 1], prices)[0])
