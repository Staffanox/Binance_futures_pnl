# Binance_futures_pnl

## Required Specifications
-   Python 3.8
-   Binance API Secret and Public key | viewing and futures permission
-   pip

___

## Setup
``git clone https://github.com/Staffanox/Binance_futures_pnl``

``cd Binance_futures_pnl``

edit ``keys`` text file in ``account``

``pip install requests``

``pip install termcolor``

___

### Output
You'll get both a .csv file and console output of overall profit in USDT

___

### Remarks

You can specify which pairs you want to analyse in ``binance/tradingPairs.py``

The more you specify the longer it takes

You can specify the start and end date for your search in ``main.py``,
simply change ``start/end`` and put them in ``pnl.printProfit()``

Duration is dependent on trading Pairs and  start/end date
