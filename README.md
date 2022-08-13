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

### Import librarys 

```python
from ejtraderCT import Ctrader

import time
import logging
from datetime import datetime

logging.getLogger().setLevel(logging.INFO)


```

### Fix login account and details

```python
server="h8.p.c-trader.cn" # Host name
broker="icmarkets" 
account="3152339"
password="393214"
currency="EUR"

api = Ctrader(server,broker,account,password,currency)
```
### Real time quote

##### Subscribe to symbol 
```python
api.subscribe("EURUSD", "GBPUSD")
```
##### All symbols quote list
```python
quote = api.quote()
print(quote)

# Output

{'EURUSD': {'bid': 1.02616, 'ask': 1.02618}, 'GBPUSD': {'bid': 1.21358, 'ask': 1.21362}}
```

#### Single symbol quote 
```python
quote = api.quote("EURUSD")
print(quote)

# Output

{'bid': 1.02612, 'ask': 1.02614}

```
### Market position and pending order.

##### Market Position

```python
# Buy position

symbol = "EURUSD"
volume = 0.01 # position size
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
#### Cancle order by id

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

#### cancel all Orders

```python
api.cancel_all()
```

#### close all positions

```python
api.close_all()
```
#### Modify Position SL and TP
```python
id = "position id "
stoploss = "stop loss price""
takeprofit "stop gain price"

api.positionModify(id, stoploss, takeprofit)

```

#### Modify order Order SL and TP and entry price
```python
id = "order id "
stoploss = "stop loss price""
takeprofit= "stop gain price"
price = "limit or stop entry price"

api.orderModify(id, stoploss, takeprofit, price)

```

# Thanks for 
@HarukaMa
@douglasbarros
