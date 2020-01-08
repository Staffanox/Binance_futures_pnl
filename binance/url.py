from urllib.parse import urljoin


def futureApi():
    return "https://fapi.binance.com"


def tradeHistoryPath():
    return "/fapi/v1/userTrades"


def joinedURL(endpoint, path):
    return urljoin(endpoint, path)
