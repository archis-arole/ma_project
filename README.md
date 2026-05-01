# Moving Average Crossover on Nifty Futures

Systematic trading research project evaluating a 9/36 MA crossover on Nifty
futures using realistic costs.

## Highlights

- 10-year backtest on Nifty Futures (2016–2026)
- Includes transaction costs, slippage, rollover assumptions
- In-sample / out-of-sample framework
- Regime-wise performance analysis
- Parameter sweep used to evaluate MA crossover combinations
- Result: strategy reduced drawdowns but failed to beat passive exposure

## Highlights

- 10-year daily backtest on Nifty Futures (2016–2026)
- Transaction costs, slippage, rollover assumptions included
- Parameter grid search across MA combinations
- Walk-forward optimization with rolling train/validation splits
- Regime analysis: Pre-COVID / COVID / Post-COVID
- Final 20% held out for out-of-sample testing
- Result: robust but lower-return strategy vs passive benchmark

## Key Result

The standalone crossover strategy did not outperform passive exposure over
2016-2026, though it showed some regime-dependent defensive characteristics.

## Strategy Equity Curve

![Equity Curve](./results/equity_curve_comparison.png)

## Drawdown Comparison

![Drawdown Curve](./results/drawdown_curve_comparison.png)

## Research Process

1. Grid searched MA fast/slow windows
2. Used walk-forward validation across rolling splits
3. Rejected unstable parameter sets dominated by single-regime performance
4. Selected 9/36 for regime consistency
5. Evaluated on untouched final test set

## Repository Structure

- `src/` source code
- `data/` datasets
- `notes/` research journal
- `results/` reports and charts

## Reports

- Parameter Optimization Report: `results/report.md`

## Reproduce

Install dependencies:

```bash
pip install -r requirements.md
```

Run from the `src/` directory:

```bash
cd src
```

Download and prepare NSE futures data:

```bash
python download.py
python extract.py
```

Run parameter search and generate report charts:

```bash
python parameter_optimization.py
```

Outputs are saved to:

```text
results/
```

## Disclaimer

Educational research only. Not investment advice.
