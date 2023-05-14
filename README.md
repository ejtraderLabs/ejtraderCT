![Pypi Publish](https://github.com/ejtraderLabs/ejtraderCT/actions/workflows/python-publish.yml/badge.svg)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/ejtraderLabs/ejtraderCT)
[![License](https://img.shields.io/github/license/ejtraderLabs/ejtraderCT)](https://github.com/ejtraderLabs/ejtraderCT/blob/master/LICENSE)
[![PyPi downloads](https://img.shields.io/pypi/dm/ejtraderCT?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/ejtraderCT/)

# Python Ctrader Fix API

`ejtraderCT` is a Python library to access the Ctrader trading platform's FIX API.

## Features

- [x] Market Position buy and sell
- [x] Pending orders limit and stop 
- [x] Partial close
- [x] Stop loss & Take profit
- [x] Modify Orders 
- [x] Modify position 
- [x] Real-time bid & ask
- [x] Check connection status
- [ ] Rest API server (in development)
- [ ] Webhook for Tradingviewer (in development)

## Prerequisites

The library has been tested on Python 3.7 to 3.9.

## Installation

To install the latest version of `ejtraderCT`, you can use pip:

```shell
pip install ejtraderCT -U
```
Or if you want to install from source, you can use:
```shell
pip install git+https://github.com/ejtraderLabs/ejtraderCT.git
```

## Accessing the Ctrader FIX API


To access your API, follow these simple steps:

1. Open the cTrader desktop or web platform.
2. In the bottom left corner of the platform, you will find the **Settings** option. Click on it.
3. A popup window will appear. In the menu of the popup, look for the last option: **FIX API**.
4. First, click on the **Change Password** button. Make sure to add a numeric password of at least 8 digits.
5. After changing the password, click on the **Copy to Clipboard** button from  **Trade Connection**.
6. Now, let's move to the **Trade Connection** section. Here, you will receive your data in the following format (this is an example with IC Markets for a real account):

   - Host name: (Current IP address 168.205.95.20 can be changed without notice)
   - Port: 5212 (SSL), 5202 (Plain text)
   - Password: (a/c 1104928 password)
   - SenderCompID: live.icmarkets.1104926 or demo.icmarkets.1104926  or live2.icmarkets.1104926 
   - TargetCompID: cServer
   - SenderSubID: TRADE





### Import libraries

```python
from ejtraderCT import Ctrader
```

### Fix account login and details

```python
server="168.205.95.20" # - Host name: (Current IP address 168.205.95.20 can be changed without notice)
account="live.icmarkets.1104926" #  - SenderCompID: live.icmarkets.1104926
password="12345678" # - The password you configured

api = Ctrader(server,account,password)

```
##### Check the connection status
```python
api.isconnected()
```
##### Logout 
```python
api.logout()
```

#### Real-time quote

##### Subscribe to symbols
```python
api.subscribe("EURUSD", "GBPUSD")
```
##### List of quotes for all symbols
```python
quote = api.quote()
print(quote)

# Output

{'EURUSD': {'bid': 1.02616, 'ask': 1.02618}, 'GBPUSD': {'bid': 1.21358, 'ask': 1.21362}}
```

#### Quote for a single symbol 
```python
quote = api.quote("EURUSD")
print(quote)

# Output

{'bid': 1.02612, 'ask': 1.02614}

```
### Market position and pending orders.

##### Market position

```python
# Buy position

symbol = "EURUSD"
volume = 0.01 # position size:
stoploss =  1.18
takeprofit = 1.19

id = api.buy(symbol, volume, stoploss, takeprofit)
print(f"Position: {id}")

# sell position 

symbol = "EURUSD"
volume = 0.01 # position size
stoploss = 1.19
takeprofit = 1.18

id = api.sell(symbol, volume, stoploss, takeprofit)
print(f"Position: {id}")
```

##### Limit Orders

```python

# Buy limit order

symbol = "EURUSD"
volume = 0.01 # order size
stoploss = 1.17
takeprofit = 1.19
price = 1.18 # entry price 

id = api.buyLimit(symbol, volume, stoploss, takeprofit, price)
print(f"Order: {id}")


# Sell limit order

symbol = "EURUSD"
volume = 0.01 # Order size
stoploss = 1.23
takeprofit = 1.17
price = 1.22 # entry price 

id = api.sellLimit(symbol, volume, stoploss, takeprofit, price)
print(f"Order: {id}")
```

#### Stop Orders

```python

# Buy stop order

symbol = "EURUSD"
volume = 0.01 # order size
stoploss = 1.20
takeprofit = 1.24
price = 1.22 # entry price

id = api.buyStop(symbol, volume, stoploss, takeprofit, price)
print(f"Order: {id}")

# Sell stop order

symbol = "EURUSD"
volume = 0.01 # order size
stoploss = 1.19
takeprofit = 1.17
price = 1.18 # entry price 

api.sellStop(symbol, volume, stoploss, takeprofit, price)

```

#### List Positions

```python
positions = api.positions()
print(positions)

```
#### List limit and stop Orders

```python
orders = api.orders()
print(orders)

```
#### Cancel order by id

```python
orders = api.orders()
for order in orders:
    api.orderCancelById(order['ord_id'])

```
#### Close position by id

```python
for position in positions:
    api.positionCloseById(position['pos_id'], position['amount'])

```

#### Cancel all orders

```python
api.cancel_all()
```

#### Close all positions

```python
api.close_all()
```
#### Modify position SL and TP
```python
id = "position id "
stoploss = "stop loss price""
takeprofit "stop gain price"

api.positionModify(id, stoploss, takeprofit)

```

#### Modify order SL and TP and entry price
```python
id = "order id "
stoploss = "stop loss price""
takeprofit= "stop gain price"
price = "limit or stop entry price"

api.orderModify(id, stoploss, takeprofit, price)

```
## Contributing

We welcome any contribution to `ejtraderCT`. Here are some ways to contribute:

1. Report issues or suggest improvements by opening an [issue](https://github.com/ejtraderLabs/ejtraderCT/issues).
2. Contribute with code to fix issues or add features via a [Pull Request](https://github.com/ejtraderLabs/ejtraderCT/pulls).

Before submitting a pull request, please make sure your codes are well formatted and tested.

## Acknowledgements

I would like to express my gratitude to [@HarukaMa](https://github.com/HarukaMa) for creating the initial project. Their work has been an invaluable starting point for my modifications and improvements.

