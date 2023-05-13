![Pypi Publish](https://github.com/ejtraderLabs/ejtraderCT/actions/workflows/python-publish.yml/badge.svg)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/ejtraderLabs/ejtraderCT)
[![License](https://img.shields.io/github/license/ejtraderLabs/ejtraderCT)](https://github.com/ejtraderLabs/ejtraderCT/blob/master/LICENSE)
[![PyPi downloads](https://img.shields.io/pypi/dm/ejtraderCT?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/ejtraderCT/)

# Python Ctrader Fix API

### ToDo

- [ ] Account Information "not possible fix limitation"
- [x] Market Position buy and sell
- [x] Peding orders limit and stop 
- [x] Partial close
- [x] Stop loss & Take profit
- [x] Modify Orders 
- [x] Modify position 
- [x] real time bid & ask


## Installation
#### Tested on python 3.7 to 3.9
```
pip install ejtraderCT -U
```
#### Or install from source

```
git clone https://github.com/ejtraderLabs/ejtraderCT
cd ejtraderCT
python setup.py install

```

### Import libraries

```python
from ejtraderCT import Ctrader

import time
import logging
from datetime import datetime

logging.getLogger().setLevel(logging.INFO)


```

### Fix account login and details

```python
server="h8.p.c-trader.cn" # Host name
broker="icmarkets" 
account="3152339"
password="393214"
currency="EUR"

api = Ctrader(server,broker,account,password,currency)

```

##### To disconnect and logout from the account
```python
api.logout()
```

### Real-time quote

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

api.buy(symbol, volume, stoploss, takeprofit)

# sell position 

symbol = "EURUSD"
volume = 0.01 # position size
stoploss = 1.19
takeprofit = 1.18

api.sell(symbol, volume, stoploss, takeprofit)
```

##### Limit Orders

```python

# Buy limit order

symbol = "EURUSD"
volume = 0.01 # position size
stoploss = 1.17
takeprofit = 1.19
price = 1.18 # entry price 

api.buyLimit(symbol, volume, stoploss, takeprofit, price)


# Sell limit order

symbol = "EURUSD"
volume = 0.01 # position size
stoploss = 1.23
takeprofit = 1.17
price = 1.22 # entry price 

api.sellLimit(symbol, volume, stoploss, takeprofit, price)
```

#### Stop Orders

```python

# Buy stop order

symbol = "EURUSD"
volume = 0.01 # position size
stoploss = 1.20
takeprofit = 1.24
price = 1.22 # entry price

api.buyStop(symbol, volume, stoploss, takeprofit, price)

# Sell stop order

symbol = "EURUSD"
volume = 0.01 # position size
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
## Contributors:

<!-- CONTRIBUTORS:START -->
<!-- CONTRIBUTORS:END -->

## Acknowledgements

I would like to express my gratitude to [@HarukaMa](https://github.com/HarukaMa) for creating the initial project. Their work has been an invaluable starting point for my modifications and improvements.
