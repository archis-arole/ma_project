import config
import requests
import logging
import datetime
from pathlib import Path

logging.basicConfig(
    filename='download.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

base1 = "https://archives.nseindia.com/content/historical/DERIVATIVES"
base2 = "https://nsearchives.nseindia.com/content/fo"
# At this date the format of filename download changed.
date_change = config.CHANGE_DATE
folder = Path("../data/bhavcopies/")
start = config.START_DATE
end = config.END_DATE
date = start

while date <= end:
    day = date.strftime("%d")
    month1 = date.strftime("%b").upper()
    month2 = date.strftime("%m")
    year = date.strftime("%Y")
    filename = config.filename(date)
    if date <= date_change:
        url = f"{base1}/{year}/{month1}/{filename}.zip"
    else:
        url = f"{base2}/{filename}.zip"

    try:
        r = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )
        if r.status_code == 200:
            with open(folder/f"{filename}.zip", 'wb') as f:
                f.write(r.content)

            logging.info(f"Downloaded {filename}.zip")
            print(f"Downloaded {filename}.zip")
        else:
            logging.warning(f"Missing {filename}")
            print(f"Missing {filename}")
    except Exception as e:
        logging.error(f"Error {filename}: {e}")
        print(f"Error {filename}: {e}")

    date += datetime.timedelta(days=1)
