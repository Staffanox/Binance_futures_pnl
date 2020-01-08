import csv
from _datetime import datetime

from binance import requests as rq
from binance import tradingPairs as tp


def realizedPNL(pnlType: rq):
    totalProfit = {i: 0 for i in tp.tradingPairs()}

    req = pnlType
    for i in range(len(req)):
        for j in range(len(req[i])):
            totalProfit[req[i][j]['symbol']] += float(req[i][j]['realizedPnl'])

    saveToCSV(totalProfit)
    return totalProfit


def printProfit(startDate=datetime.now(), endDate=datetime.now()):
    sumTotal = 0
    if startDate != datetime.now() and endDate != datetime.now():
        print("Profits from", datetime.fromtimestamp(startDate / 1e3), "to", datetime.fromtimestamp(endDate / 1e3))
        print()
        totalProfit = realizedPNL(rq.pnlRequestSeveralDays(startDate, endDate))
    else:
        totalProfit = realizedPNL(rq.pnlRequest(rq.hashedParams(rq.params())))
    for x in totalProfit:
        if totalProfit[x] < 0:
            print("Total loss for", x, "is", totalProfit[x], "USDT")
        else:
            print("Total profit for", x, "is", totalProfit[x], "USDT")
        sumTotal += totalProfit[x]
    print("Total Pnl is ", sumTotal, 'USDT')


def saveToCSV(totalProfit):
    with open('tradeProfit.csv', mode='w') as csv_file:
        fieldnames = ['Asset', 'Profit']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for i in totalProfit:
            writer.writerow({fieldnames[0]: i, fieldnames[1]: totalProfit[i]})
