import datetime

from calc import handle_time as ht
from calc import pnl

# default is profits from start of 2020 (current year) to now
# date is given in year, month, day order

current_date = datetime.datetime.now()
start, end = ht.dates(current_date.year, 1, 1, current_date.year, current_date.month, current_date.day)

# Put start and end in here to specify the range of your calculated Profits, the duration depends on the size of
# duration and trades during specified range
# That's because Binance only allows start and end time to be 24h apart
# With four trading pairs that's 1460 requests to the api each differing in response time due to varying trade size

profit = pnl.get_profit_for_date(start,end)
print(profit)
