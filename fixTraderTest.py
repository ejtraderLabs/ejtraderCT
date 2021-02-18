import sys
sys.path.append('../') 
import time
import logging
from datetime import datetime


from ejtrader_ct import CtraderFix

FIX_SERVER="h8.p.c-trader.cn"
FIX_BROKER="icmarkets"
FIX_LOGIN="3152339"
FIX_PASSWORD="393214"
FIX_CURRENCY="EUR"


logging.getLogger().setLevel(logging.INFO)


CtraderFix = CtraderFix(FIX_SERVER,FIX_BROKER,FIX_LOGIN,FIX_PASSWORD,FIX_CURRENCY)
# 
# accountInfo = CtraderFix.accountInfo()
# print(accountInfo)
# print(accountInfo['broker'])
# print(accountInfo['balance'])

# time.sleep(1)

# CtraderFix.buy("GBPUSD", 0.01, 1.18, 1.19)
# CtraderFix.sell("GBPUSD", 0.01, 1.19, 1.18)


# time.sleep(1)

# positions = CtraderFix.positions()
# print(positions)
# for position in positions:
#     CtraderFix.positionCloseById(position['pos_id'], position['amount'])


time.sleep(1)

# CtraderFix.buyLimit("GBPUSD", 0.01, 1.17, 1.19, 1.18)
# CtraderFix.sellLimit("GBPUSD", 0.01, 1.23, 1.17, 1.22)
# CtraderFix.buyStop("GBPUSD", 0.01, 1.20, 1.24, 1.22)
# CtraderFix.sellStop("GBPUSD", 0.01, 1.19, 1.17, 1.18)

time.sleep(1)


orders = CtraderFix.orders()
print(orders)
for order in orders:
    CtraderFix.orderCancelById(order['ord_id'])

# positions = CtraderFix.positions()
# print(positions)

# CtraderFix.close_all()
# CtraderFix.cancel_all()

# history = CtraderFix.history("GBPUSD", "M5", int(datetime.now().timestamp()) - 10000)
# print(history)