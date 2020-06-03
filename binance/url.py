from urllib.parse import urljoin

from account import keys


def futureApi():
    return "https://fapi.binance.com"


def tradeHistoryPath():
    return "/fapi/v1/userTrades"


def joinedURL(endpoint, path):
    return urljoin(endpoint, path)


def apiHeader():
    return {"X-MBX-APIKEY": keys.public_key()}
