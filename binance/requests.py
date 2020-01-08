import time
from datetime import datetime

import requests

from account import keys, hashKeys
from binance import url, tradingPairs as tp


def dates(startyear, startmonth, startday, endyear, endmonth, endday):
    startdate = int(datetime(startyear, startmonth, startday).timestamp() * 1000)
    enddate = int(datetime(endyear, endmonth, endday).timestamp() * 1000)
    if startdate > enddate:
        raise TypeError("Start can't be after end")
    else:
        return startdate, enddate


def apiHeader():
    return {"X-MBX-APIKEY": keys.publicKey()}


def params():
    parameters = []
    timestamp = int(time.time() * 1000)
    for i in tp.tradingPairs():
        parameters.append({'symbol': i,
                           'timestamp': timestamp})
    return parameters


def paramsWithDate(startdate: dates, enddate: dates):
    parameters = []
    timestamp = int(time.time() * 1000)
    for i in tp.tradingPairs():
        parameters.append({'symbol': i,
                           'startTime': startdate,
                           'endTime': enddate,
                           'timestamp': timestamp})
    return parameters


def hashedParams(parameters: list):
    for i in range(len(parameters)):
        parameters[i]['signature'] = hashKeys.hashIt(parameters)[i]
    return parameters


def pnlRequest(hashedPar: list):
    request = []
    for i in hashedPar:
        request.append(requests.get(url=url.joinedURL(url.futureApi(), url.tradeHistoryPath()), params=i,
                                    headers=apiHeader()).json())

    return request


def pnlRequestSeveralDays(start: dates, end: dates):
    realstartdate, realenddate = start, end
    startdate = realstartdate
    enddate = startdate + 86400000
    request = []
    while startdate < realenddate:
        # todo could be recursive and better

        rq = pnlRequest(hashedParams(paramsWithDate(startdate, enddate)))
        rqs = [x for x in rq if x]
        if rqs:
            request.append(rqs)
        startdate += 86400000
        enddate = startdate + 86400000

    # flattens the list because a dict burrowed in three sublists is cancer

    flat_list = [item for sublist in request for item in sublist]

    return flat_list
