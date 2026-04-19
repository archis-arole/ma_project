import model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

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


def train_validate(chunk_num):
    front_training = pd.concat(front_chunks[:chunk_num], ignore_index=True)
    next_training = pd.concat(next_chunks[:chunk_num], ignore_index=True)
    front_validation = front_chunks[chunk_num].reset_index(drop=True)
    next_validation = next_chunks[chunk_num].reset_index(drop=True)
    return front_training, next_training, front_validation, next_validation


def base(sp_lower_bound, sp_upper_bound,
         lp_lower_bound, lp_upper_bound):
    short_periods = np.arange(sp_lower_bound, sp_upper_bound)
    long_periods = np.arange(lp_lower_bound, lp_upper_bound)
    S, L = np.meshgrid(short_periods, long_periods, indexing='ij')
    grid = np.stack([S, L], axis=-1).reshape(-1, 2)
    return grid


def metric_list(front_df, next_df, sp_lower_bound, sp_upper_bound,
                lp_lower_bound, lp_upper_bound, metric):
    grid = base(sp_lower_bound, sp_upper_bound,
                lp_lower_bound, lp_upper_bound)
    if metric == 'mean':
        r = 0
    elif metric == 'volatility':
        r = 1
    elif metric == 'sharpe':
        r = 2
    elif metric == 'CAGR':
        r = 3
    elif metric == 'max_drawdown':
        r = 4
    else:
        raise ValueError('the only possible values of metric'
                         ' are sharpe, CAGR or max_drawdown.')
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


ft, nt, fv, nv = train_validate(6)
metric_heatmap(fv, nv, 10, 30, 30, 100, 'sharpe',
               'validation_sharpe_2')
