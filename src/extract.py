import config
import utils
import os
import logging
from pathlib import Path
import datetime
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='extract.log'
)
logger = logging.getLogger(__name__)

folder = Path('../data/bhavcopies/')
start = config.START_DATE
end = config.END_DATE
change_date = config.CHANGE_DATE
date = start
front_month_rows = []
next_month_rows = []
skipped = 0
logger.info(f"Starting extraction: {start} to {end}")

while date <= end:
    name = config.filename(date)
    if name in os.listdir(folder):
        df = pd.read_csv(folder/name)
    else:
        date += datetime.timedelta(days=1)
        logger.debug(f"File not found, skipping: {name}")
        skipped += 1
        continue

    if date <= change_date:
        df = df.rename(columns={
            'TIMESTAMP': 'DATE',
            'INSTRUMENT': 'INSTRUMENT',
            'SYMBOL': 'SYMBOL',
            'EXPIRY_DT': 'EXPIRY',
            'SETTLE_PR': 'PRICE',
            'OPEN_INT': 'OI'
        })
        filt = (
            (df['INSTRUMENT'] == 'FUTIDX') &
            (df['SYMBOL'] == 'NIFTY')
        )
        cols_needed = ['DATE', 'EXPIRY', 'PRICE', 'OI']
        contracts = df.loc[filt, cols_needed].sort_values('EXPIRY')
        contracts['DATE'] = pd.to_datetime(
            contracts['DATE'], format='%d-%b-%Y').dt.strftime('%Y-%m-%d')
        contracts['EXPIRY'] = pd.to_datetime(
            contracts['EXPIRY'], format='%d-%b-%Y').dt.strftime('%Y-%m-%d')
        front_row = contracts.iloc[0:1]
        next_row = contracts.iloc[1:2]

    else:
        df = df.rename(columns={
            'BizDt': 'DATE',
            'FinInstrmTp': 'INSTRUMENT',
            'TckrSymb': 'SYMBOL',
            'FininstrmActlXpryDt': 'EXPIRY',
            'SttlmPric': 'PRICE',
            'OpnIntrst': 'OI'
        })
        filt = (
            (df['INSTRUMENT'] == 'IDF') &
            (df['SYMBOL'] == 'NIFTY')
        )
        cols_needed = ['DATE', 'EXPIRY', 'PRICE', 'OI']
        contracts = df.loc[filt, cols_needed].sort_values('EXPIRY')
        front_row = contracts.iloc[0:1]
        next_row = contracts.iloc[1:2]

    if front_row.empty or next_row.empty:
        logger.warning(f"Missing front or next contract on {date}")
    else:
        logger.info(f"Successfully extracted {name}")

    front_month_rows.append(front_row)
    next_month_rows.append(next_row)
    date += datetime.timedelta(days=1)

logger.info(f"Loop complete - {len(front_month_rows)} trading days processed,"
            f" {skipped} files skipped")

front_df = pd.concat(front_month_rows, ignore_index=True)
next_df = pd.concat(next_month_rows, ignore_index=True)
logger.info(f"front_df: {len(front_df)} rows, {front_df['DATE'].min()} "
            f"to {front_df['DATE'].max()}")
logger.info(f"next_df:  {len(next_df)} rows, {next_df['DATE'].min()} "
            f"to {next_df['DATE'].max()}")
front_df.to_csv('../data/processed/front_month_futures.csv')
next_df.to_csv('../data/processed/next_month_futures.csv')
logger.info("CSVs saved: front_month_futures.csv, next_month_futures.csv")
utils.view(front_df)
utils.view(next_df)
