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

- Details: I have used nifty $50$ daily futures data for the last $10$ years.
by downloading NSE bhavcopies from them.
I have implemented a rollover scheme based on
open interest of the market and have not used any other adjustments.

- What I did next: Include transaction costs like
STT, slippage, rollover costs, etc.

## Transaction costs (v3.0)

- What I did: I included transaction costs resulting from
STT, slippage and rollover of futures in the core model.

- Details: I ran the model using these parameters:

    - Short window of crossover: $7$ days
    - Long window of crossover: $21$ days
    - STT rate: $0.05\%$ for every sell position
    - Slippage rate: $0.02\%$ for every trade

I ran the model for crossover on prices
which is recorded in the Prices column
and for crossover on returns, recorded in the returns column.

| Metric      | Prices    | Returns   |
|-------------|-----------|-----------|
| Mean Return | -0.000125 | -0.000242 |
| Volatility  |  0.010372 |  0.010373 |
| Sharpe      | -0.190954 | -0.371077 |
| CAGR        | -0.043963 | -0.071858 |
| Max Drawdown| -0.449314 | -0.548304 |

Mean return refers to the mean of daily returns using the model.
Volatility refers to the standard deviation of daily returns using the model.
Sharpe ratio is annualized (by taking a year to be $252$ days).
CAGR means the Compounded Annual Growth Rate of the model.
Max Drawdown refers to the maximum drawdown of returns using the model.

We observe that both models return negative return.
Here, we observe that crossover over prices beats returns
after we include transaction costs
[but not before](#price-vs-returns-v2.3).

What I will do next: I will optimize my parameters
and also optimize my portfolio of futures.

## Parameter optimization

- Goal: To pick optimum parameters,
which in this case are the short period window
and the long period window of the moving average crossover model.

- Method: Grid search and intuitive feelings
to pick the correct parameters in order to avoid
one-off successes with specific parameters.
I also used walk-forward validation to avoid overfitting
and not fall for early misleading signals.

- Note: I had already tried to implement it
[earlier](#optimization-of-parameters-v2.0),
but I didn't complete even one stage of the validation
when I realized the [major mistake](#major-mistake-v2.1)
that my model wasn't realistic.

- Details: The dataset has been roughly divided
into ten equal chunks. I am training on $80\%$ of the data
and will have the final test of the model using $20\%$ of the data.
I also have $3$ stages of walk-forward validation.
The first stage trains on $50\%$ of the data and is validated
on the next $10\%$ of the data.
We then walk forward by $10\%$ of the data to get $3$ stages.

### First stage

- What I did: I implemented heatmaps of various metrics
like Sharpe ratio, maximum drawdown and CAGR
with respect to varying windows of the moving average crossover model.
I also implemented walk-forward validation to avoid overfitting.

- Observations: In all the heatmaps I plotted,
I could clearly see that there is a $5$ by $5$ grid,
where the short window period was between $20$ and $25$,
and long one was between $50$ and $55$.

- Results: I finally picked the parameters.
I used $22$ days for the short period window
and $52$ days for the long period window.
Here is the table describing the results of
the model on the training dataset:

| Metrics | Value |
|---|---|
| Mean Return | 0.000900 |
| Volatility | 0.011791 |
| Sharpe | 1.211976 |
| CAGR | 0.232909 |
| Max Drawdown | -0.252587 |

And these are the results of the model on the validation dataset:

| Metric | Value |
|---|---|
| Mean Return | -0.000386 |
| Volatility | 0.010434 |
| Sharpe | -0.587502 |
| CAGR | -0.105025 |
| Max Drawdown | -0.224653 |

- What went wrong: My model appears to be instable with regime changes.
This is discovered in the second stage of walk-forward validation.

### Second stage

- What I did: After plotting the heatmaps for this stage,
I also remembered that I could use the equity curve
to track the growth of my equity.

- Observation: Many of the models having good results,
have actually only done really well in one financial year
which was April $2020$ to April $2021$.
This is consistent with the way nifty had a good bull run
during this period which is when COVID struck.

- Details: I plotted the equity curves for
a few combinations of long period and short period parameters,
like $(22, 52)$, $(30, 40)$ and $(15, 70)$.
These all had good sharpe in the training dataset
and all the equity curves followed the same pattern
as laid out in our observation.

- What I will do next: I will evaluate the model
separately for the pre-COVID, COVID and post-COVID regimes.
Here the COVID regime refers to only that one financial year
from April $2020$ to April $2021$.

### Third stage

- What I did: I plotted heatmaps of the metrics
for $3$ regimes, pre-COVID, COVID and post-COVID regimes.
On that basis, I chose parameters which had greatest regime stability
over parameters which had better sharpe only due to the COVID regime.

- Observation: Many combinations of these parameters
have one regime where there is negative sharpe.
It's either pre-COVID or post-COVID.
It is interesting to note that the pre-COVID regime
favoured models which were slower to change
while the post-COVID regime favoured models which were faster to change.

- Results: These are the results of the original model
with fast moving average of $22$ days
and slow moving average of $52$ days.

| Metric       | Pre-COVID Regime | COVID Regime | Post-COVID Regime |
| ------------ | ---------------: | -----------: | ----------------: |
| Mean Return  |         0.000629 |     0.001916 |         -0.000613 |
| Volatility   |         0.011532 |     0.011115 |          0.009769 |
| Sharpe       |         0.865953 |     2.736985 |         -0.996307 |
| CAGR         |         0.152448 |     0.595159 |         -0.153415 |
| Max Drawdown |        -0.186039 |    -0.073561 |         -0.370126 |

It is clear that this model is dangerous to use
in the post-COVID regime and hence we reject this model
even if it maximizes sharpe overall.

I observed that there is only one small region
which maintained positive sharpe throughout regimes.
Out of this region, I took a sample where
the fast moving average was for $9$ days and
the slow moving average was for $36$ days.
These are the results of that model:

| Metric       | Pre-COVID Regime | COVID Regime | Post-COVID Regime | Validation |
| ------------ | ---------------: | -----------: | ----------------: | ---------: |
| Mean Return  |         0.000340 |     0.000824 |          0.000050 |   0.000141 |
| Volatility   |         0.011474 |     0.011367 |          0.009652 |   0.006641 |
| Sharpe       |         0.470271 |     1.151024 |          0.082433 |   0.337521 |
| CAGR         |         0.071659 |     0.210937 |          0.000936 |   0.030508 |
| Max Drawdown |        -0.270137 |    -0.169462 |         -0.176477 |  -0.108726 |
