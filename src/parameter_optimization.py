import model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

# Split into 9 sequential chunks: first 8 with 246 rows, last with the rest.
front_df = pd.read_csv('../data/processed/front_month_futures.csv')
next_df = pd.read_csv('../data/processed/next_month_futures.csv')
raw_data = model.rollover(front_df, next_df)[0]
roll_indices = model.rollover(front_df, next_df)[1]
data = raw_data.copy()
chunks = np.array_split(data, 10)
training_data = pd.concat(chunks[:5], ignore_index=True)
prices = training_data["PRICE"]
returns = prices.pct_change().dropna()
baseline_mean_return = returns.mean()
baseline_volatility = returns.std(ddof=1)
baseline_sharpe_ratio = baseline_mean_return / baseline_volatility

short_periods = np.arange(7, 15)
long_periods = np.arange(15, 30)
S, L = np.meshgrid(short_periods, long_periods, indexing="ij")
grid = np.stack([S, L], axis=-1).reshape(-1, 2)
sharpes = [model.model_stats(row[0], row[1], front_df, next_df).iloc[2, 1]
           for row in grid]
print(sharpes)

'''
plt.figure(figsize=(8, 6))
plt.imshow(
    sharpes,
    origin="lower",
    aspect="auto",
    cmap="viridis",
    vmin=-0.05,
    vmax=0.10,
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
plt.show()
'''
