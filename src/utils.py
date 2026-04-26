import matplotlib.pyplot as plt
import subprocess
import pandas as pd


def view(df: pd.DataFrame):
    """View df in sc-im"""
    filename = "df_output.csv"
    df.to_csv(filename, index=False)
    subprocess.run(["visidata", "-r", filename])


def plot_equity_curve(equity_curve):
    """Plot the equity curve over time and return figure."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(equity_curve.index, equity_curve.values)
    ax.set_xlabel("Date")
    ax.set_ylabel("Equity")
    ax.set_title("Equity Curve")
    fig.tight_layout()
    return fig


def plot_equity_curve_comparison(strategy_curve, benchmark_curve):
    """Plot strategy vs benchmark equity curves and return figure."""
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(strategy_curve.index, strategy_curve.values, label="MA Strategy")
    ax.plot(benchmark_curve.index, benchmark_curve.values, label="Passive Benchmark")

    ax.set_xlabel("Date")
    ax.set_ylabel("Equity")
    ax.set_title("Equity Curve: Strategy vs Passive")
    ax.legend()

    fig.tight_layout()
    return fig


def plot_drawdown_curve(equity_curve):
    """Plot drawdown curve from an equity curve and return figure."""
    running_peak = equity_curve.cummax()
    drawdown = (equity_curve / running_peak) - 1

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(drawdown.index, drawdown.values)

    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdown")
    ax.set_title("Drawdown Curve")

    fig.tight_layout()
    return fig


def plot_drawdown_curve_comparison(strategy_curve, benchmark_curve):
    """Plot strategy vs benchmark drawdown curves and return figure."""
    strategy_peak = strategy_curve.cummax()
    strategy_dd = (strategy_curve / strategy_peak) - 1

    benchmark_peak = benchmark_curve.cummax()
    benchmark_dd = (benchmark_curve / benchmark_peak) - 1

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(strategy_dd.index, strategy_dd.values, label="MA Strategy")
    ax.plot(benchmark_dd.index, benchmark_dd.values, label="Passive Benchmark")

    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdown")
    ax.set_title("Drawdown Curve: Strategy vs Passive")
    ax.legend()

    fig.tight_layout()
    return fig
