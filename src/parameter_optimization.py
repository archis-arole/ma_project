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
front_training = pd.concat(front_chunks[:5], ignore_index=True)
next_training = pd.concat(next_chunks[:5], ignore_index=True)

short_periods = np.arange(10, 30)
long_periods = np.arange(30, 100)
S, L = np.meshgrid(short_periods, long_periods, indexing="ij")
grid = np.stack([S, L], axis=-1).reshape(-1, 2)
sharpes = [model.model_stats(
    row[0], row[1], front_training, next_training
).iloc[2, 1] for row in grid]
sharpes = np.array(sharpes).reshape(len(short_periods), len(long_periods))

plt.figure(figsize=(8, 6))
plt.imshow(
    sharpes,
    origin="lower",
    aspect="auto",
    cmap="viridis",
    vmin=sharpes.min(),
    vmax=sharpes.max(),
    extent=[
        long_periods.min(),
        long_periods.max(),
        short_periods.min(),
        short_periods.max(),
    ]
)
plt.colorbar(label="Sharpe")
plt.xlabel("Long Period")
plt.ylabel("Short Period")
plt.title("Sharpe Heatmap")
plt.tight_layout()
plt.savefig('../results/parameter_optimize/sharpe_ratio_broad_view_1.png',
            dpi=150, bbox_inches='tight')
plt.show()
