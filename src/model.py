import numpy as np
import pandas as pd
pd.set_option('future.no_silent_downcasting', True)


def rollover(front_df, next_df):
    '''
    Build an unadjusted continuous series using OI crossover.
    Returns:
    - combined_df: chosen rows from front/next
    - roll_indices: integer indices where roll happens
    '''
    required_cols = ['DATE', 'EXPIRY', 'PRICE', 'OI']
    df = pd.merge(
        front_df[required_cols],
        next_df[required_cols],
        on='DATE',
        suffixes=('_front', '_next'),
    ).sort_values('DATE')

    roll_trigger = df['OI_next'] > df['OI_front']
    use_next = roll_trigger.groupby(df['EXPIRY_front']).cummax()
    roll_start = use_next & ~use_next.shift(1).fillna(False)
    roll_indices = list(df.index[roll_start])
    combined_df = df.copy()
    combined_df['EXPIRY'] = df['EXPIRY_front'].where(
        ~use_next, df['EXPIRY_next']
    )
    combined_df['PRICE'] = df['PRICE_front'].where(
        ~use_next, df['PRICE_next']
    )
    combined_df['OI'] = df['OI_front'].where(
        ~use_next, df['OI_next']
    )
    combined_df = combined_df[['DATE', 'EXPIRY', 'PRICE', 'OI']]
    return combined_df, roll_indices


def model(sp, lp, front_df, next_df, slippage_bps=0.0002, stt_rate=0.0005):
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

    ma_short = prices.rolling(sp).mean().shift(1)[lp + 1:]
    ma_long = prices.rolling(lp).mean().shift(1)[lp + 1:]
    signal = ma_long < ma_short
    position = pd.Series(
        np.where(signal, 1, -1), index=signal.index
    )
    position_change = position.diff().fillna(0)

    returns_aligned = returns.reindex(signal.index).dropna()
    model_returns = returns_aligned * np.where(
        signal, 1, -1
    )

    roll_flag = pd.Series(
        model_returns.index.isin(roll_indices),
        index=model_returns.index
    )
    trade_size = position_change.abs()
    extra_roll = roll_flag & (trade_size == 0)

    legs = trade_size + 2 * extra_roll.astype(int)
    slippage_cost = slippage_bps * legs

    sell_legs = (-position_change).clip(lower=0) + extra_roll.astype(int)
    stt_cost = stt_rate * sell_legs

    cost = slippage_cost + stt_cost

    net_returns = model_returns - cost
    equity_curve = (1 + net_returns).cumprod()
    trades = (position_change != 0).sum()

    return equity_curve, net_returns, trades


def model_stats(sp, lp, front_df, next_df,
                slippage_bps=0.0002, stt_rate=0.0005):
    equity_curve, model_returns, trades = model(sp, lp, front_df, next_df,
                                                slippage_bps, stt_rate)
    equity = equity_curve.iloc[-1]
    mean_returns = model_returns.mean()
    std_returns = model_returns.std(ddof=1)
    sharpe_ratio = mean_returns / std_returns * np.sqrt(252)
    years = len(equity_curve) / 252
    CAGR = equity ** (1 / years) - 1
    running_max = equity_curve.cummax()
    drawdown = equity_curve / running_max - 1
    max_drawdown = drawdown.min()
    calmar_ratio = CAGR / np.abs(max_drawdown)
    trade_percent = trades / years
    metrics = [
        'Mean Return',
        'Volatility',
        'Sharpe',
        'CAGR',
        'Max Drawdown',
        'Calmar',
        'Trades/year',
    ]
    values = [
        mean_returns,
        std_returns,
        sharpe_ratio,
        CAGR,
        max_drawdown,
        calmar_ratio,
        trade_percent
    ]
    metrics_df = pd.DataFrame(
        {'metrics': metrics, 'value': values}
    )
    return metrics_df


def baseline(front_df, next_df,
             slippage_bps=0.0002, stt_rate=0.0005):
    df, roll_indices = rollover(front_df, next_df)
    prices = df['PRICE']
    returns = prices.pct_change().dropna()

    roll_flag = pd.Series(
        returns.index.isin(roll_indices),
        index=returns.index
    )
    legs = 2 * roll_flag
    sell_legs = roll_flag
    entry_flag = pd.Series(0, index=returns.index)
    entry_flag.iloc[0] = 1

    slippage_cost = slippage_bps * legs
    stt_cost = stt_rate * sell_legs
    entry_slippage = slippage_bps * entry_flag
    cost = slippage_cost + stt_cost + entry_slippage

    net_returns = returns - cost
    equity_curve = (1 + net_returns).cumprod()

    return equity_curve, net_returns


def baseline_stats(front_df, next_df,
                   slippage_bps=0.0002, stt_rate=0.0005):
    equity_curve, net_returns = baseline(front_df, next_df,
                                         slippage_bps=0.0002, stt_rate=0.0005)
    equity = equity_curve.iloc[-1]
    mean_returns = net_returns.mean()
    std_returns = net_returns.std(ddof=1)
    sharpe_ratio = mean_returns / std_returns * np.sqrt(252)
    years = len(equity_curve) / 252
    CAGR = equity ** (1 / years) - 1
    running_max = equity_curve.cummax()
    drawdown = equity_curve / running_max - 1
    max_drawdown = drawdown.min()
    calmar_ratio = CAGR / np.abs(max_drawdown)
    metrics = [
        'Mean Return',
        'Volatility',
        'Sharpe',
        'CAGR',
        'Max Drawdown',
        'Calmar',
    ]
    values = [
        mean_returns,
        std_returns,
        sharpe_ratio,
        CAGR,
        max_drawdown,
        calmar_ratio,
    ]
    metrics_df = pd.DataFrame(
        {'metrics': metrics, 'value': values}
    )
    return metrics_df
