import csv
import os

from termcolor import colored

from binance import requests as req
from binance import tradingPairs as t


def map_pnl(pnl_type: req):

    total_profit = {i: 0 for i in t.tradingPairs()}
    request = pnl_type

    for day in request:
        for trade in day:
            total_profit[trade['symbol']] += float(trade['realizedPnl'])
    os.chdir("..")
    save_to_csv(total_profit)
    return total_profit


def map_time_and_pnl(request: req, time_range):

    total_profit = {i: 0 for i in time_range}

    for i in request:
        if i:
            total_profit[i['time']] += float(i['realizedPnl'])

    return total_profit


def get_profit_for_date(start_date=None, end_date=None):

    if start_date is not None and end_date is not None and start_date > end_date:
        raise TypeError("Start can't be after end")

    if start_date is not None and end_date is not None:
        return map_pnl(req.pnl_custom_range(start_date, end_date))

    elif isinstance(start_date, str):
        request = req.analyse(start_date)
        return map_time_and_pnl(request[1], request[0])

    else:
        return map_pnl(req.pnl_request(req.hashed_params(req.params())))


def print_profit(totalProfit: dict):

    sum_total = 0

    for x in totalProfit:

        if totalProfit[x] < 0:
            print("Total loss for", x, "is", colored(totalProfit[x], 'red'), "USDT")

        elif totalProfit[x] == 0:
            print("Total profit for", x, "is", colored(totalProfit[x], 'white'), "USDT")

        else:
            print("Total profit for", x, "is", colored(totalProfit[x], 'green'), "USDT")

        sum_total += totalProfit[x]
    if sum_total > 0:
        print("Total Pnl is ", colored(sum_total, 'green'), 'USDT')

    elif sum_total < 0:
        print("Total Pnl is ", colored(sum_total, 'red'), 'USDT')

    else:
        print("Total Pnl is ", sum_total, 'USDT')


def save_to_csv(total_profit):

    with open('tradeProfit.csv', mode='w') as csv_file:

        fieldnames = ['Asset', 'Profit']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for i in total_profit:
            writer.writerow({fieldnames[0]: i, fieldnames[1]: total_profit[i]})
