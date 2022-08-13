# Python Ctrader Fix API

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
SERVER="h8.p.c-trader.cn"
BROKER="icmarkets"
LOGIN="3152339"
PASSWORD="393214"
CURRENCY="EUR"

api = Ctrader(SERVER,BROKER,LOGIN,PASSWORD,CURRENCY)
```
### Real time quote

##### Subscribe to symbol 
```python
api.symbolSubscribe("EURUSD", "GBPUSD")
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
api.buy("EURUSD", 0.01, 1.18, 1.19)
api.sell("EURUSD", 0.01, 1.19, 1.18)
```

##### Limit Orders 

```python
api.buyLimit("EURUSD", 0.01, 1.17, 1.19, 1.18)
api.sellLimit("EURUSD", 0.01, 1.23, 1.17, 1.22)
```

#### Stop Orders

```python
api.buyStop("EURUSD", 0.01, 1.20, 1.24, 1.22)
api.sellStop("EURUSD", 0.01, 1.19, 1.17, 1.18)
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

#### Modify order Order SL and TP
```python
id = "order id "
stoploss = "stop loss price""
takeprofit "stop gain price"

api.orderModify(id, stoploss, takeprofit, price)

```

### ToDo

- [ ] Account Information
- [x] Partial close
- [x] SL and TP
- [x] Modify Orders 
- [x] Modify position 
- [x] real time bid & ask

# Thanks for 
@HarukaMa
@douglasbarros
