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
    For now this model does not use leverage.
    So we remain entirely invested only with the equity we have.

    Inputs:
    params: It is an array of 2 numbers: sp and lp in that order
    front_df: It is the DataFrame of the front month futures
    next_df: It is the DataFrame of the next month futures
    '''
    df, roll_indices = rollover(front_df, next_df)
    prices = df['PRICE']
    returns = prices.pct_change()
    sp, lp = params

    ma_short = prices.rolling(sp).mean().shift(1)[lp + 1:]
    ma_long = prices.rolling(lp).mean().shift(1)[lp + 1:]
    signal = ma_long < ma_short
    position = pd.Series(
        np.where(signal, 1, -1), index=signal.index
    )
    position_change = position.diff().fillna(0)
    trade = signal.ne(signal.shift(1))
    trade.iloc[0] = True

    returns_aligned = returns.reindex(signal.index).dropna()
    model_returns = returns_aligned * np.where(
        signal, 1, -1
    )

    cost = pd.Series(0.0, index=model_returns.index)
    slippage_bps = 0.0002
    cost += slippage_bps * trade.astype(float)

    cost = pd.Series(0.0, index=model_returns.index)
    stt_rate = 0.0005
    sell_amount = (-position_change).clip(lower=0)
    cost += stt_rate * sell_amount

    roll_flag = pd.Series(
        model_returns.index.isin(roll_indices),
        index=model_returns.index
    )
    cost += 2 * slippage_bps * roll_flag.astype(float)  # exit + entry
    cost += stt_rate * roll_flag.astype(float)           # sell leg

    net_returns = model_returns - cost
    equity_curve = (1 + net_returns).cumprod()

    return equity_curve, net_returns


front_df = pd.read_csv('../data/processed/front_month_futures.csv')
next_df = pd.read_csv('../data/processed/next_month_futures.csv')
model([7, 21], front_df, next_df)
