import requests
import datetime
from pathlib import Path

base1 = "https://archives.nseindia.com/content/historical/DERIVATIVES"
base2 = "https://nsearchives.nseindia.com/content/fo"
# At this date the format of filename download changed.
date_change = datetime.date(2024, 7, 5)
folder = Path("../data/bhavcopies/")
start = datetime.date(2024, 7, 1)
end = datetime.date(2024, 8, 1)
date = start

while date <= end:
    day = date.strftime("%d")
    month1 = date.strftime("%b").upper()
    month2 = date.strftime("%m")
    year = date.strftime("%Y")
    if date <= date_change:
        filename = f"fo{day}{month1}{year}bhav.csv.zip"
        url = f"{base1}/{year}/{month1}/{filename}"
    else:
        filename = f"BhavCopy_NSE_FO_0_0_0_{year}{month2}{day}_F_0000.csv.zip"
        url = f"{base2}/{filename}"

    try:
        r = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
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
