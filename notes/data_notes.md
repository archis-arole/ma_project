On july 5 2024, the data format completely changed.

Old datasets:
1. INSTRUMENT = "FUTIDX"
2. SYMBOL = "NIFTY"
3. EXPIRY_DT
4. TIMESTAMP
5. SETTLE_PR
6. OPEN_INT
7. Filename: foDDMMMYYYYbhav.csv (like 'fo22APR2024bhav.csv)
8. Date format: DD-MMM-YYYY (like 22-APR-2024)

New datasets:
1. FinInstrmTp = "IDF"
2. TckrSymb = "NIFTY"
3. FininstrmActlXpryDt = expiry date
4. BizDt
5. SttlmPric
6. OpnIntrst
7. Filename: Bhavcopy_NSE_FO_0_0_0_YYYYMMDD_F_0000.csv
8: Date format: YYYY-MM-DD
