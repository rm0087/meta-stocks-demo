from datetime import datetime, timedelta
import requests

headers = {
        "Content-Type" : "application/json",
        "Accept" : "application/json",
        'APCA-API-KEY-ID': "PK28C1IX5GA5YGO8PUC1",
        'APCA-API-SECRET-KEY': "82uB25KPmQD09O7abyr5U5ZYFdb02tQC11aOUlgL"
    }


end = datetime.now() - timedelta(hours=-24)
f_end = end.strftime("%Y-%m-%dT%H")
start = datetime.now() - timedelta(hours=-25)
f_start = start.strftime("%Y-%m-%dT%H")

r = requests.get(f'https://data.alpaca.markets/v2/stocks/bars?symbols=AAPL&timeframe=1Day&limit=5&adjustment=raw&feed=sip&sort=desc', headers=headers)
print(r.status_code, r.text)