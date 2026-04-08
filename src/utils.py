import matplotlib.pyplot as plt


def plot_equity_curve(equity_curve):
    """Plot the equity curve over time."""
    plt.figure(figsize=(10, 5))
    plt.plot(equity_curve.index, equity_curve.values)
    plt.xlabel("Date")
    plt.ylabel("Equity")
    plt.title("Equity Curve")
    plt.tight_layout()
    plt.show()
