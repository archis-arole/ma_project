# Research journal

## Basic model (v1.0)

- What I did: My model idea was to use the moving averages of a longer period
versus a moving average of a shorter period as a signal for trading.

- What was the mistake: I used only long position and never took any short position.
It gives a misleading sharpe ratio because volatility decreases
if you trade on lesser days, and mean can be 'handpicked' to remain strong.
These are the results of the first model:

| metric | baseline | model |
| --- | --- | --- |
| mean | 0.0003 | 0.0006 |
| volatility | 0.0077 | 0.0059 |
| sharpe ratio | 0.0359 | 0.1012 |

- What I did next: Made a proper signal and put both long positions
and short positions depending on the signal.

- Details: For this version, I used the nifty $50$ daily returns data.
Daily returns were calculated on the current and previous *close* data.
Positions were squared off at the next close and re-entered independently each day.

## Long-short model (v1.5)

- What I did: I now added both a long and short position
according to the signal at that time.

- What was the mistake: I ignored the na values at the start
of the moving average lists which distorted the sharpe ratio.
So, even when the mean return of only the long position days
was $0.06\%$ and $-0.03\%$ return on days where I shorted,
the mean of the overall strategy was oddly $0.02\%$.
The results of the model are shown below:

| metric | baseline | model |
| --- | --- | --- |
| mean | 0.0003 | 0.0002 |
| volatility | 0.0077 | 0.0077 |
| sharpe ratio | 0.0358 | 0.0310 |

- What I did next: I made a separate function called model
and fixed the na error bug while parametrizing my code for the future.

## Final model (v1.6)

- What I did: I fixed the na bug and then proceeded
to parametrize the model for future training of the model.
These are the final results of the model:

| metric | baseline | model |
| --- | --- | --- |
| mean | 0.0003 | 0.0005 |
| volatility | 0.0077 | 0.0070 |
| sharpe ratio | 0.0358 | 0.0652 |

- Details: The model was structured as follows:

    - Signal: Moving average over $21$ days < Moving average over $7$ days.

    - If signal is true, we buy one unit and then square off
    the position immediately the same day.

    - Else, we sell or short one unit and then square off
    the position immediately the same day.

- What I did next: I am now going to optimize parameters
for the model to maximize the sharpe ratio.

## Optimization of parameters (v2.0)

- What I did: I have changed my dataset to
daily data of the last $10$ years of nifty.
Then, I split it into chunks, and divided
the dataset into training and test datasets
while implementing walk-forward validation.
This has been done to prevent overfitting of parameters.

- Details: I am using an $80$-$20$ split for training and test datasets.
I am initially training with $50\%$ of the dataset and using $10\%$
increments for walk-forward validation.

- What I did next: I decided to use a grid search for parameter optimization
in order to prevent overfitting by trying to test every parameter.
In order to do this, I will plot heatmaps of the parameter meshgrid
I have created, where color is decided according to sharpe ratio.

## Major mistake found (v2.1)

- What I did: I started training on my first training dataset.
I plotted various heatmaps of to see which regions in the heatmaps
had better sharpe ratio than others (inputs were parameters).

- What was the mistake: I did not factor in transaction costs.
I also squared off my position every single day,
which not only results in no compounding of returns,
but also results in huge transaction costs.
Moreover I realized that I cannot short stocks easily.

- What I will do next: I will rewrrite the model to include transaction costs.
I will now use futures data instead of stocks data.
I will also not square off every single day and instead
I will square off every time my position changes
and hold my position otherwise.

## Price vs returns (v2.3)

- What I did: I tweaked the model so that it can incorporate
the model involving a crossover signal based on returns as well as prices.
Moreover, it outputs the compounded return at the end.

- Observation: I ran it on the last year nifty 50 daily stock data
just to see whether it changes anything out of curiosity.
It had the opposite effect of what I expected.
The crossover model using returns earned $5\%$,
while the crossover model using prices *lost* $11\%$.
Of course, this is no conclusion, but just an interesting observation.

- What I did next: I have added another hold position
so that I don't square off every single day
and then I have also included an equity curve
for better tracking and enhanced metrics.

## Rollover and data pipeline (v2.6)

- What I did: I included futures data and extracted
the front month and next month datasets from it.
I also implemented rollover in my core model.

- Details: I have used nifty 50 daily futures data
by downloading NSE bhavcopies from them.
I have implemented a rollover scheme based on
open interest of the market and have not used any other adjustments.

- What I did next: Include transaction costs like
STT, slippage, rollover costs, etc.

## Transaction costs (v3.0)

- What I did: I included transaction costs resulting from
STT, slippage and rollover of futures in the core model.

- Observation: I ran the model using these parameters:

    - Short window of crossover: $7$ days
    - Long window of crossover: $21$ days
    - STT rate: $0.05\%$ for every sell position
    - Slippage rate: $0.02\%$ for every trade

These are the results for crossover over prices:

        metrics     value
0   Mean Return -0.000125
1    Volatility  0.010372
2        Sharpe -0.190954
3          CAGR -0.043963
4  Max Drawdown -0.449314

These are the results for crossover over returns:

        metrics     value
0   Mean Return -0.000242
1    Volatility  0.010373
2        Sharpe -0.371077
3          CAGR -0.071858
4  Max Drawdown -0.548304
