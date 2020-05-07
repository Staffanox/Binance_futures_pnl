import time
import requests
import datetime
from datetime import timedelta
from account import keys, hashKeys
from binance import url, tradingPairs as tp
from calc import handleTime as ht

formatter = ht.good_formatter


def apiHeader():
    return {"X-MBX-APIKEY": keys.public_key()}


def params(start_date=None, end_date=None):
    parameters = []
    for pair in tp.tradingPairs():
        timestamp = int(time.time() * 1e3)
        if start_date is not None and end_date is not None:
            parameters.append({'symbol': pair,
                               'startTime': start_date,
                               'endTime': end_date,
                               'timestamp': timestamp})
        else:
            parameters.append({'symbol': pair,
                               'timestamp': timestamp})
    return parameters


def hashedParams(parameters: list):
    for i in parameters:
        i['signature'] = hashKeys.hashIt(i)
    return parameters


def pnlRequest(hashed_par: list):
    request = []
    for i in hashed_par:
        request.append(requests.get(url=url.joinedURL(url.futureApi(), url.tradeHistoryPath()), params=i,
                                    headers=apiHeader()).json())

    if 'msg' in request[0]:
        raise TypeError(request[0]['msg'])
    else:
        return request


def pnl_custom_range(start: int, end: int):
    start_date, real_end_date = start, end
    request = []
    while start_date <= real_end_date:
        req = pnlRequest(hashedParams(params(start_date, int(start_date + timedelta(days=1).total_seconds() * 1e3))))
        for trade in req:
            if trade:
                request.append(trade)
        start_date += int(timedelta(days=1).total_seconds() * 1e3)

    # flattens the list because a dict burrowed in three sublists is cancer
    #flat_list = [item for sublist in request for item in sublist]
    #flat_list = [item for sublist in flat_list for item in sublist]

    return request


def analyse(date_range: str):
    time_range = []
    request = []
    # todo pattern matching
    # todo function body : find whats same, abstract that into function and give variable parameters into function parameters
    if date_range == 'week':
        start, end = ht.range_of_week()
        start = datetime.datetime.strptime(start, formatter)
        end = datetime.datetime.strptime(end, formatter)
        while start < end:
            time_range.append(start)
            request.append(
                pnl_custom_range(int(datetime.datetime.timestamp(start)), int(datetime.datetime.timestamp(end))))
            start += datetime.timedelta(days=1)
    elif date_range == 'month':
        start, end = ht.range_of_month()
        start = datetime.datetime.strptime(start, formatter)
        end = datetime.datetime.strptime(end, formatter)
        while start < end:
            time_range.append(start)
            request.append(
                pnl_custom_range(int(datetime.datetime.timestamp(start)), int(datetime.datetime.timestamp(end))))
            start += datetime.timedelta(days=1)
    elif date_range == 'year':
        start, end = ht.range_of_year()
        start = datetime.datetime.strptime(start, formatter)
        end = datetime.datetime.strptime(end, formatter)
        while start < end:
            time_range.append(start.strftime(formatter))
            request.append(
                pnl_custom_range(int(datetime.datetime.timestamp(start)), int(datetime.datetime.timestamp(end))))
            start += datetime.timedelta(days=1)
    return time_range, request
