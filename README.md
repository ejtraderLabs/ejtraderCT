# Python Ctrader Fix API

## Installation

```
pip install ejtrader_ct

or

python setup.py install

```

### import

```python
from ejtrader_ct import CtraderFix

import time
import logging
from datetime import datetime

logging.getLogger().setLevel(logging.INFO)


```

### Fix login account and details

```python
FIX_SERVER="h8.p.c-trader.cn"
FIX_BROKER="icmarkets"
FIX_LOGIN="3152339"
FIX_PASSWORD="393214"
FIX_CURRENCY="EUR"

CtraderFix = CtraderFix(FIX_SERVER,FIX_BROKER,FIX_LOGIN,FIX_PASSWORD,FIX_CURRENCY)

```

### You can create market or pending order with the commands.

#### Market Orders

```python
CtraderFix.buy("EURUSD", 0.01, 1.18, 1.19)
```

```python
CtraderFix.sell("EURUSD", 0.01, 1.19, 1.18)
```

#### Limit Orders

```python
CtraderFix.buyLimit("EURUSD", 0.01, 1.17, 1.19, 1.18)
CtraderFix.sellLimit("EURUSD", 0.01, 1.23, 1.17, 1.22)
```

#### Stop Orders

```python
CtraderFix.buyStop("EURUSD", 0.01, 1.20, 1.24, 1.22)
CtraderFix.sellStop("EURUSD", 0.01, 1.19, 1.17, 1.18)
```

#### Positions

```python
positions = CtraderFix.positions()
print(positions)
for position in positions:
    CtraderFix.positionCloseById(position['pos_id'], position['amount'])

positions = CtraderFix.positions()
print(positions)

```

## Orders Manipulation

```python
Corders = CtraderFix.orders()
print(orders)
for order in orders:
    CtraderFix.orderCancelById(order['ord_id'])

orders = CtraderFix.orders()
print(orders)

```

#### If you want to cancel all Orders

```python
CtraderFix.cancel_all()
```

#### if you want to close all positions

```python
CtraderFix.close_all()
```

### Future add comming soon

Modify pending orders

```python
CtraderFix.modify()

```

Real time Data and history

```python
history = CtraderFix.history("GBPUSD", "M5", int(datetime.now().timestamp()) - 10000)
# print(history)

```

Account information

```python
accountInfo = CtraderFix.accountInfo()
print(accountInfo)
print(accountInfo['broker'])
print(accountInfo['balance'])

```
