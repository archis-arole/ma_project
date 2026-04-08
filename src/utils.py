import matplotlib.pyplot as plt
import subprocess
import pandas as pd


def view(df: pd.DataFrame):
    ''' View df in sc-im '''
    filename = "df_output.csv"
    df.to_csv(filename, index=False)
    subprocess.run(["sc-im", "-r", filename])


def plot_equity_curve(equity_curve):
    """Plot the equity curve over time."""
    plt.figure(figsize=(10, 5))
    plt.plot(equity_curve.index, equity_curve.values)
    plt.xlabel("Date")
    plt.ylabel("Equity")
    plt.title("Equity Curve")
    plt.tight_layout()
    plt.show()
