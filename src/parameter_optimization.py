import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()


def model_summary(params, returns):
    model_mean_return, model_volatility, model_sharpe_ratio = model(
        params, returns
    )
    summary_df = pd.DataFrame(
        [
            {
                "mean": baseline_mean_return,
                "volatility": baseline_volatility,
                "sharpe ratio": baseline_sharpe_ratio,
            },
            {
                "mean": model_mean_return,
                "volatility": model_volatility,
                "sharpe ratio": model_sharpe_ratio,
            },
        ],
        index=["baseline", "model"],
    ).round(4)
    return summary_df


raw_data = pd.read_csv("./nifty50_last_10_years.csv")
data = raw_data.copy()

# Split into 9 sequential chunks: first 8 with 246 rows, last with the rest.
chunks = np.array_split(data, 10)
training_data = pd.concat(chunks[:5], ignore_index=True)
close_prices = training_data["Close"]
returns = close_prices.pct_change().dropna()
baseline_mean_return = returns.mean()
baseline_volatility = returns.std(ddof=1)
baseline_sharpe_ratio = baseline_mean_return / baseline_volatility

short_periods = np.arange(7, 15)
long_periods = np.arange(15, 30)
long_positions = np.arange(1, 10)
S, L, P = np.meshgrid(short_periods, long_periods,
                      long_positions, indexing="ij")
grid = np.stack([S, L, P], axis=-1).reshape(-1, 3)
results = [model(row, returns)[2] for row in grid]
sharpes = np.array(results).reshape(S.shape)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection="3d")
sc = ax.scatter(
    S.ravel(),
    L.ravel(),
    P.ravel(),
    c=sharpes.ravel(),
    cmap="viridis",
    vmin=-0.05,
    vmax=0.10,
    s=25,
)
ax.set_xlabel("Short Period")
ax.set_ylabel("Long Period")
ax.set_zlabel("Long/Short Ratio")
ax.set_title("Sharpe Ratio Map")
fig.colorbar(sc, ax=ax, label="Sharpe")
plt.tight_layout()
plt.show()

fixed_ratio = 1
ratio_idx = np.where(long_positions == fixed_ratio)[0]
if len(ratio_idx) == 0:
    raise ValueError("fixed_ratio not found in long_positions")
ratio_idx = ratio_idx[0]

plt.figure(figsize=(8, 6))
plt.imshow(
    sharpes[:, :, ratio_idx],
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
    ],
)
plt.colorbar(label="Sharpe")
plt.xlabel("Long Period")
plt.ylabel("Short Period")
plt.title(f"Sharpe Heatmap (Long/Short Ratio = {fixed_ratio})")
plt.tight_layout()
plt.show()
