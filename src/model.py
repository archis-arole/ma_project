import numpy as np
import utils
import pandas as pd


def rollover(front_df, next_df):
    '''
    Build an unadjusted continuous series using OI crossover.
    Returns:
    - combined_df: chosen rows from front/next
    - roll_indices: integer indices where roll happens
    '''
    required_cols = ["DATE", "EXPIRY", "PRICE", "OI"]
    df = pd.merge(
        front_df[required_cols],
        next_df[required_cols],
        on="DATE",
        suffixes=("_front", "_next"),
    ).sort_values("DATE")

    roll_trigger = df["OI_next"] > df["OI_front"]
    use_next = roll_trigger.groupby(df["EXPIRY_front"]).cummax()
    roll_start = use_next & ~use_next.shift(1).fillna(False)
    roll_indices = list(df.index[roll_start])
    combined_df = df.copy()
    combined_df["EXPIRY"] = df["EXPIRY_front"].where(
        ~use_next, df["EXPIRY_next"]
    )
    combined_df["PRICE"] = df["PRICE_front"].where(
        ~use_next, df["PRICE_next"]
    )
    combined_df["OI"] = df["OI_front"].where(
        ~use_next, df["OI_next"]
    )
    combined_df = combined_df[["DATE", "EXPIRY", "PRICE", "OI"]]
    return combined_df, roll_indices


def model(params, front_df, next_df):
    '''
    This is the moving average model.
    sp is short period of moving average.
    lp is long period of moving average.
    Also expects long/short ratio.
    Note that this function is vectorized.
    '''
    combined_df, roll_indices = rollover(front_df, next_df)
    prices = combined_df['PRICE']
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


front_df = pd.read_csv('../data/processed/front_month_futures.csv')
next_df = pd.read_csv('../data/processed/next_month_futures.csv')
utils.view(rollover(front_df, next_df)[0])
print(rollover(front_df, next_df)[1])
# print(model_stats([7, 21, 1], prices))
# utils.plot_equity_curve(model([7, 21, 1], prices)[0])
