import matplotlib.pyplot as plt
import subprocess
import pandas as pd


def view(df: pd.DataFrame):
    ''' View df in sc-im '''
    filename = "df_output.csv"
    df.to_csv(filename, index=False)
    subprocess.run(["sc-im", "-r", filename])


def plot_equity_curve(equity_curve):
    """Plot the equity curve over time and return figure."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(equity_curve.index, equity_curve.values)
    ax.set_xlabel("Date")
    ax.set_ylabel("Equity")
    ax.set_title("Equity Curve")
    fig.tight_layout()
    return fig
