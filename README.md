
### ToDo

- [ ] SL and TP
- [ ] Thread Save
- [ ] real time bid & ask
# Python Ctrader Fix API

## Installation

```
pip install ejtraderCT -U

or

python setup.py install

```

## import

```python
from ejtraderCT import Ctrader

import time
import logging
from datetime import datetime

logging.getLogger().setLevel(logging.INFO)


```

## Fix login account and details

```python
FIX_SERVER="h8.p.c-trader.cn"
FIX_BROKER="icmarkets"
FIX_LOGIN="3152339"
FIX_PASSWORD="393214"
FIX_CURRENCY="EUR"

api = Ctrader(FIX_SERVER,FIX_BROKER,FIX_LOGIN,FIX_PASSWORD,FIX_CURRENCY)

```

### You can create market or pending order with the commands.

## Market Orders

```python
api.buy("EURUSD", 0.01, 1.18, 1.19)
api.sell("EURUSD", 0.01, 1.19, 1.18)
```

## Limit Orders

```python
api.buyLimit("EURUSD", 0.01, 1.17, 1.19, 1.18)
api.sellLimit("EURUSD", 0.01, 1.23, 1.17, 1.22)
```

## Stop Orders

```python
api.buyStop("EURUSD", 0.01, 1.20, 1.24, 1.22)
api.sellStop("EURUSD", 0.01, 1.19, 1.17, 1.18)
```

## Positions

```python
positions = api.positions()
print(positions)
for position in positions:
    api.positionCloseById(position['pos_id'], position['amount'])

positions = api.positions()
print(positions)

```

## Orders Manipulation

```python
Corders = api.orders()
print(orders)
for order in orders:
    api.orderCancelById(order['ord_id'])

orders = api.orders()
print(orders)

```

## cancel all Orders

```python
api.cancel_all()
```

## close all positions

```python
api.close_all()
```

# Future add comming soon

Modify pending orders

```python
api.modify()

```

Real time Data and history

```python
history = api.history("GBPUSD", "M5", int(datetime.now().timestamp()) - 10000)
# print(history)

```

Account information

```python
accountInfo = api.accountInfo()
print(accountInfo)
print(accountInfo['broker'])
print(accountInfo['balance'])

```




# Thanks for 
@HarukaMa
@douglasbarros
