import datetime
import time
from datetime import timedelta

import requests

from account import hashKeys
from binance import url, tradingPairs as tp
from binance.url import apiHeader
from calc import handle_time as ht


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


def hashed_params(parameters: list):

    for i in parameters:
        i['signature'] = hashKeys.hashIt(i)
    return parameters


def pnl_request(hashed_par: list):

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
        req = pnl_request(hashed_params(params(start_date, int(start_date + timedelta(days=1).total_seconds() * 1e3))))
        for trade in req:
            if trade:
                request.append(trade)
        start_date += int(timedelta(days=1).total_seconds() * 1e3)

    return request


def analyse(date_range: str):

    time_range = []
    request = []

    if date_range == 'week':

        start, end = ht.range_of_week()

        while start < end:
            time_range.append(start.date().strftime(ht.formatter))
            request.append(
                pnl_custom_range(ht.create_timestamp(start), ht.create_timestamp(end)))
            start += datetime.timedelta(days=1)

    elif date_range == 'month':

        start, end = ht.range_of_month()

        while start < end:
            time_range.append(start.date().strftime(ht.formatter))
            request.append(
                pnl_custom_range(ht.create_timestamp(start), ht.create_timestamp(end)))
            start += datetime.timedelta(days=1)

    elif date_range == 'year':

        start, end = ht.range_of_year()

        while start < end:
            time_range.append(start.date().strftime(ht.formatter))
            request.append(
                pnl_custom_range(ht.create_timestamp(start), ht.create_timestamp(end)))
            start += datetime.timedelta(days=1)

    return time_range, request
