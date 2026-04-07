import datetime

# CHANGE_DATE is the date when data format of bhavcopy changed.
# Note that July 5 2024, is the last day the old format
# was used and not the day the format changed which is July 8
# (July 6 and July 7 is a weekend)
CHANGE_DATE = datetime.date(2024, 7, 5)
START_DATE = datetime.date(2016, 4, 6)
END_DATE = datetime.date(2026, 4, 6)


def filename(date):
    day = date.strftime("%d")
    month1 = date.strftime("%b").upper()
    month2 = date.strftime("%m")
    year = date.strftime("%Y")
    if date <= CHANGE_DATE:
        name = f"fo{day}{month1}{year}bhav.csv.zip"
    else:
        name = f"BhavCopy_NSE_FO_0_0_0_{year}{month2}{day}_F_0000.csv.zip"
    return name
