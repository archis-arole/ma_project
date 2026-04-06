import requests
import datetime
import time
from pathlib import Path

BASE = "https://archives.nseindia.com/content/historical/DERIVATIVES"
folder = Path("../data/bhavcopies/")
start = datetime.date(2024, 7, 1)
end = datetime.date(2025, 8, 1)
date = start

while date <= end:
    day = date.strftime("%d")
    month = date.strftime("%b").upper()
    year = date.strftime("%Y")
    filename = f"fo{day}{month}{year}bhav.csv.zip"
    url = f"{BASE}/{year}/{month}/{filename}"

    try:
        r = requests.get(
            url,
            timeout=10
        )
        if r.status_code == 200:
            with open(folder/filename, 'wb') as f:
                f.write(r.content)

            print("Downloaded:", filename)
        else:
            print("Missing:", filename)
    except Exception as e:
        print("Error:", filename, e)

    date += datetime.timedelta(days=1)
    time.sleep(0.5)
