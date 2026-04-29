# Moving Average Crossover on Nifty Futures

Systematic trading research project evaluating a 9/36 MA crossover on Nifty
futures using realistic costs.

## Highlights

- 10-year backtest on Nifty Futures (2016–2026)
- Includes transaction costs, slippage, rollover assumptions
- In-sample / out-of-sample framework
- Regime-wise performance analysis
- Result: strategy reduced drawdowns but failed to beat passive exposure

## Key Result

The standalone crossover strategy did not outperform passive exposure over
2016-2026, though it showed some regime-dependent defensive characteristics.

## Strategy Equity Curve

![Equity Curve](./results/parameter_optimize/equity_curve_comparison.png)

## Drawdown Comparison

![Drawdown Curve](./results/parameter_optimize/drawdown_curve_comparison.png)

## Reports

- Parameter Optimization Report: `results/parameter_optimize/report.md`

## Repository Structure

- `src/` source code
- `data/` datasets
- `notes/` research journal
- `results/` reports and charts

## Disclaimer

Educational research only. Not investment advice.
