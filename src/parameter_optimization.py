import model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import utils

sns.set()


def base(sp_lower_bound, sp_upper_bound,
         lp_lower_bound, lp_upper_bound):
    short_periods = np.arange(sp_lower_bound, sp_upper_bound)
    long_periods = np.arange(lp_lower_bound, lp_upper_bound)
    S, L = np.meshgrid(short_periods, long_periods, indexing='ij')
    grid = np.stack([S, L], axis=-1).reshape(-1, 2)
    return grid


def metric_list(front_df, next_df, sp_lower_bound, sp_upper_bound,
                lp_lower_bound, lp_upper_bound, metric):

    metric_map = {
        'mean': 0,
        'volatility': 1,
        'sharpe': 2,
        'CAGR': 3,
        'max_drawdown': 4,
        'calmar': 5,
        'trades': 6
    }

    try:
        r = metric_map[metric]
    except KeyError:
        raise ValueError('Invalid metric name.')

    grid = base(sp_lower_bound, sp_upper_bound,
                lp_lower_bound, lp_upper_bound)
    metrics = [model.model_stats(
        row[0], row[1], front_df, next_df
    ).iloc[r, 1] for row in grid]
    metrics = np.array(metrics).reshape(
        sp_upper_bound - sp_lower_bound,
        lp_upper_bound - lp_lower_bound
    )
    return metrics


def metric_heatmap(front_df, next_df, sp_lower_bound, sp_upper_bound,
                   lp_lower_bound, lp_upper_bound, metric, filename):
    metrics = metric_list(front_df, next_df,
                          sp_lower_bound, sp_upper_bound,
                          lp_lower_bound, lp_upper_bound, metric)
    plt.figure(figsize=(8, 6))
    plt.imshow(
        metrics,
        origin='lower',
        aspect='auto',
        cmap='viridis',
        vmin=metrics.min(),
        vmax=metrics.max(),
        extent=[
            lp_lower_bound,
            lp_upper_bound,
            sp_lower_bound,
            sp_upper_bound
        ]
    )
    plt.colorbar(label=f'{metric}')
    plt.xlabel('Long Period')
    plt.ylabel('Short Period')
    plt.title(f'{metric} heatmap')
    plt.tight_layout()
    plt.savefig(f'../results/parameter_optimize/{filename}.png',
                dpi=150, bbox_inches='tight')
    plt.show()


chunk_num = 8
sp_lower_bound = 1
sp_upper_bound = 20
lp_lower_bound = 20
lp_upper_bound = 50
sp = 9
lp = 36

# Split into 9 sequential chunks:
# first 8 with 10% of rows, last with the rest.
raw_front_df = pd.read_csv('../data/processed/front_month_futures.csv')
raw_next_df = pd.read_csv('../data/processed/next_month_futures.csv')
front_df = raw_front_df.copy()
next_df = raw_next_df.copy()
front_chunks = np.array_split(front_df, 10)
next_chunks = np.array_split(next_df, 10)
front_test = pd.concat(front_chunks[8:], ignore_index=True)
next_test = pd.concat(next_chunks[8:], ignore_index=True)

# f and n means front and next month futures
# and t and v mean training and validation
# and pre and post mean pre and post covid regimes
ft_pre = pd.concat(front_chunks[:4], ignore_index=True)
nt_pre = pd.concat(next_chunks[:4], ignore_index=True)
ft_covid = front_chunks[4].reset_index(drop=True)
nt_covid = next_chunks[4].reset_index(drop=True)
ft_post = pd.concat(front_chunks[5:chunk_num], ignore_index=True)
nt_post = pd.concat(next_chunks[5:chunk_num], ignore_index=True)

strategy_curve = model.model(sp, lp, front_df, next_df)[0]
benchmark_curve = model.baseline(front_df, next_df)[0]
fig1 = utils.plot_drawdown_curve_comparison(strategy_curve, benchmark_curve)
fig2 = utils.plot_equity_curve_comparison(strategy_curve, benchmark_curve)
fig1.savefig('../results/parameter_optimize/drawdown_curve_comparison.png')
fig2.savefig('../results/parameter_optimize/equity_curve_comparison.png')
