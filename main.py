from datetime import datetime

from binance import requests as rq
from calc import pnl

date = datetime.now()

# default is profits from start of 2020 (current year) to now
# date is given in year month day order

start, end = rq.dates(2020, 1, 1, date.year, date.month, date.day)

# Put start and end in here to specify the range of your calculated Profits, the duration depends on the size of
# duration and trades during specified range
# That's because Binance only allows start and end time to be 24h apart
# With four trading pairs that's 1460 requests to the api each differing in response time due to varying trade size

pnl.printProfit()
