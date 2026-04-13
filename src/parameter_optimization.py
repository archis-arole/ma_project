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
    S, L = np.meshgrid(short_periods, long_periods, indexing="ij")
    grid = np.stack([S, L], axis=-1).reshape(-1, 2)
    return grid


def sharpe_list(chunk_num, sp_lower_bound, sp_upper_bound,
                lp_lower_bound, lp_upper_bound):
    '''
    Plots heatmap of sharpe ratio given various parameters:
    chunk_num: This refers to how much of the data is now
    included under training in the walk forward validation scheme
    sp means short window of moving average crossover,
    and lp is the long window.
    It's lower and upper bounds define the extent of the heatmap
    Finally, we have the filename argument, which saves
    the plot in the filename we choose in ../results/parameter_optimize/
    '''
    front_training = train_validate(chunk_num)[0]
    next_training = train_validate(chunk_num)[1]
    grid = base(sp_lower_bound, sp_upper_bound,
                lp_lower_bound, lp_upper_bound)
    sharpes = [model.model_stats(
        row[0], row[1], front_training, next_training
    ).iloc[2, 1] for row in grid]
    sharpes = np.array(sharpes).reshape(
        sp_upper_bound - sp_lower_bound,
        lp_upper_bound - lp_lower_bound
    )
    return sharpes


def sharpe_heatmap(chunk_num, sp_lower_bound, sp_upper_bound,
                   lp_lower_bound, lp_upper_bound, filename):
    sharpes = sharpe_list(chunk_num, sp_lower_bound, sp_upper_bound,
                          lp_lower_bound, lp_upper_bound)
    plt.figure(figsize=(8, 6))
    plt.imshow(
        sharpes,
        origin="lower",
        aspect="auto",
        cmap="viridis",
        vmin=sharpes.min(),
        vmax=sharpes.max(),
        extent=[
            lp_lower_bound,
            lp_upper_bound,
            sp_lower_bound,
            sp_upper_bound
        ]
    )
    plt.colorbar(label="Sharpe")
    plt.xlabel("Long Period")
    plt.ylabel("Short Period")
    plt.title("Sharpe Heatmap")
    plt.tight_layout()
    plt.savefig(f'../results/parameter_optimize/{filename}.png',
                dpi=150, bbox_inches='tight')
    plt.show()


sharpe_heatmap(5, 10, 30, 30, 100, 'test')
