
### ToDo

- [ ] SL and TP
- [ ] Thread Save
- [x] real time bid & ask
# Python Ctrader Fix API

## Installation
Tested on python 3.7 and 3.8
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
SERVER="h8.p.c-trader.cn"
BROKER="icmarkets"
LOGIN="3152339"
PASSWORD="393214"
CURRENCY="EUR"

api = Ctrader(SERVER,BROKER,LOGIN,PASSWORD,CURRENCY)



```
### New function Real time Quote
Real time quote

```python
api.symbolSubscribe("EURUSD", "GBPUSD")

# All symbols Quote list

quote = api.quote()
print(quote)
{'EURUSD': {'bid': 1.02616, 'ask': 1.02618}, 'GBPUSD': {'bid': 1.21358, 'ask': 1.21362}}


# Single symbol Quote 
quote = api.quote("EURUSD")
print(quote)

{'bid': 1.02612, 'ask': 1.02614}

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



Account information

```python
accountInfo = api.accountInfo()
print(accountInfo)
print(accountInfo['broker'])
print(accountInfo['balance'])

```

SYMBOL LIST AND IDS

```json
'default': {
        1: {'id': 1, 'pip_position': 4, 'name': 'EURUSD', 'bid_volume': 0, 'ask_volume': 0},
        2: {'id': 2, 'pip_position': 4, 'name': 'GBPUSD', 'bid_volume': 0, 'ask_volume': 0},
        3: {'id': 3, 'pip_position': 2, 'name': 'EURJPY', 'bid_volume': 0, 'ask_volume': 0},
        4: {'id': 4, 'pip_position': 2, 'name': 'USDJPY', 'bid_volume': 0, 'ask_volume': 0},
        5: {'id': 5, 'pip_position': 4, 'name': 'AUDUSD', 'bid_volume': 0, 'ask_volume': 0},
        6: {'id': 6, 'pip_position': 4, 'name': 'USDCHF', 'bid_volume': 0, 'ask_volume': 0},
        7: {'id': 7, 'pip_position': 2, 'name': 'GBPJPY', 'bid_volume': 0, 'ask_volume': 0},
        8: {'id': 8, 'pip_position': 4, 'name': 'USDCAD', 'bid_volume': 0, 'ask_volume': 0},
        9: {'id': 9, 'pip_position': 4, 'name': 'EURGBP', 'bid_volume': 0, 'ask_volume': 0},
        10: {'id': 10, 'pip_position': 4, 'name': 'EURCHF', 'bid_volume': 0, 'ask_volume': 0},
        11: {'id': 11, 'pip_position': 2, 'name': 'AUDJPY', 'bid_volume': 0, 'ask_volume': 0},
        12: {'id': 12, 'pip_position': 4, 'name': 'NZDUSD', 'bid_volume': 0, 'ask_volume': 0},
        13: {'id': 13, 'pip_position': 2, 'name': 'CHFJPY', 'bid_volume': 0, 'ask_volume': 0},
        14: {'id': 14, 'pip_position': 4, 'name': 'EURAUD', 'bid_volume': 0, 'ask_volume': 0},
        15: {'id': 15, 'pip_position': 2, 'name': 'CADJPY', 'bid_volume': 0, 'ask_volume': 0},
        16: {'id': 16, 'pip_position': 4, 'name': 'GBPAUD', 'bid_volume': 0, 'ask_volume': 0},
        17: {'id': 17, 'pip_position': 4, 'name': 'EURCAD', 'bid_volume': 0, 'ask_volume': 0},
        18: {'id': 18, 'pip_position': 4, 'name': 'AUDCAD', 'bid_volume': 0, 'ask_volume': 0},
        19: {'id': 19, 'pip_position': 4, 'name': 'GBPCAD', 'bid_volume': 0, 'ask_volume': 0},
        20: {'id': 20, 'pip_position': 4, 'name': 'AUDNZD', 'bid_volume': 0, 'ask_volume': 0},
        21: {'id': 21, 'pip_position': 2, 'name': 'NZDJPY', 'bid_volume': 0, 'ask_volume': 0},
        22: {'id': 22, 'pip_position': 4, 'name': 'USDNOK', 'bid_volume': 0, 'ask_volume': 0},
        23: {'id': 23, 'pip_position': 4, 'name': 'AUDCHF', 'bid_volume': 0, 'ask_volume': 0},
        24: {'id': 24, 'pip_position': 4, 'name': 'USDMXN', 'bid_volume': 0, 'ask_volume': 0},
        25: {'id': 25, 'pip_position': 4, 'name': 'GBPNZD', 'bid_volume': 0, 'ask_volume': 0},
        26: {'id': 26, 'pip_position': 4, 'name': 'EURNZD', 'bid_volume': 0, 'ask_volume': 0},
        27: {'id': 27, 'pip_position': 4, 'name': 'CADCHF', 'bid_volume': 0, 'ask_volume': 0},
        28: {'id': 28, 'pip_position': 4, 'name': 'USDSGD', 'bid_volume': 0, 'ask_volume': 0},
        29: {'id': 29, 'pip_position': 4, 'name': 'USDSEK', 'bid_volume': 0, 'ask_volume': 0},
        30: {'id': 30, 'pip_position': 4, 'name': 'NZDCAD', 'bid_volume': 0, 'ask_volume': 0},
        31: {'id': 31, 'pip_position': 4, 'name': 'EURSEK', 'bid_volume': 0, 'ask_volume': 0},
        32: {'id': 32, 'pip_position': 4, 'name': 'GBPSGD', 'bid_volume': 0, 'ask_volume': 0},
        33: {'id': 33, 'pip_position': 4, 'name': 'EURNOK', 'bid_volume': 0, 'ask_volume': 0},
        34: {'id': 34, 'pip_position': 4, 'name': 'EURHUF', 'bid_volume': 0, 'ask_volume': 0},
        35: {'id': 35, 'pip_position': 4, 'name': 'USDPLN', 'bid_volume': 0, 'ask_volume': 0},
        36: {'id': 36, 'pip_position': 4, 'name': 'USDDKK', 'bid_volume': 0, 'ask_volume': 0},
        37: {'id': 37, 'pip_position': 4, 'name': 'GBPNOK', 'bid_volume': 0, 'ask_volume': 0},
        39: {'id': 39, 'pip_position': 4, 'name': 'NZDCHF', 'bid_volume': 0, 'ask_volume': 0},
        40: {'id': 40, 'pip_position': 4, 'name': 'GBPCHF', 'bid_volume': 0, 'ask_volume': 0},
        43: {'id': 43, 'pip_position': 4, 'name': 'USDTRY', 'bid_volume': 0, 'ask_volume': 0},
        44: {'id': 44, 'pip_position': 4, 'name': 'EURTRY', 'bid_volume': 0, 'ask_volume': 0},
        46: {'id': 46, 'pip_position': 4, 'name': 'EURZAR', 'bid_volume': 0, 'ask_volume': 0},
        47: {'id': 47, 'pip_position': 2, 'name': 'SGDJPY', 'bid_volume': 0, 'ask_volume': 0},
        48: {'id': 48, 'pip_position': 4, 'name': 'USDHKD', 'bid_volume': 0, 'ask_volume': 0},
        49: {'id': 49, 'pip_position': 4, 'name': 'USDZAR', 'bid_volume': 0, 'ask_volume': 0},
        50: {'id': 50, 'pip_position': 4, 'name': 'EURMXN', 'bid_volume': 0, 'ask_volume': 0},
        51: {'id': 51, 'pip_position': 4, 'name': 'EURPLN', 'bid_volume': 0, 'ask_volume': 0},
        53: {'id': 53, 'pip_position': 4, 'name': 'NZDSGD', 'bid_volume': 0, 'ask_volume': 0},
        54: {'id': 54, 'pip_position': 4, 'name': 'USDHUF', 'bid_volume': 0, 'ask_volume': 0},
        55: {'id': 55, 'pip_position': 4, 'name': 'EURCZK', 'bid_volume': 0, 'ask_volume': 0},
        56: {'id': 56, 'pip_position': 4, 'name': 'USDCZK', 'bid_volume': 0, 'ask_volume': 0},
        57: {'id': 57, 'pip_position': 4, 'name': 'EURDKK', 'bid_volume': 0, 'ask_volume': 0},
        60: {'id': 60, 'pip_position': 4, 'name': 'USDCNH', 'bid_volume': 0, 'ask_volume': 0},
        61: {'id': 61, 'pip_position': 4, 'name': 'GBPSEK', 'bid_volume': 0, 'ask_volume': 0},
    },

```




Calculate spread

```python
from ejtraderCT import calculate_spread, SYMBOLSLIST

symbol_table = SYMBOLSLIST['default']
symbol_id = 1 # EURUSD
spread = calculate_spread(
            'bid',
            'ask',symbol_table[int(symbol_id)]['pip_position']
        )

```




# Thanks for 
@HarukaMa
@douglasbarros
