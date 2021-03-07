
import time
import logging
from datetime import datetime


from ejtraderCT import Ctrader

FIX_SERVER="h8.p.c-trader.cn"
FIX_BROKER="icmarkets"
FIX_LOGIN="3152339"
FIX_PASSWORD="393214"
FIX_CURRENCY="EUR"


logging.getLogger().setLevel(logging.INFO)


api = Ctrader(FIX_SERVER,FIX_BROKER,FIX_LOGIN,FIX_PASSWORD,FIX_CURRENCY)
# 
# accountInfo = api.accountInfo()
# print(accountInfo)
# print(accountInfo['broker'])
# print(accountInfo['balance'])

#time.sleep(1)

clid_buy = api.buy("GBPUSD", 0.01, 1.18, 1.19)
clid_sell = api.sell("GBPUSD", 0.01, 1.19, 1.18)

api.buyLimit("GBPUSD", 0.01, 1.17, 1.19, 1.18)
api.sellLimit("GBPUSD", 0.01, 1.23, 1.17, 1.22)
api.buyStop("GBPUSD", 0.01, 1.20, 1.24, 1.22)
api.sellStop("GBPUSD", 0.01, 1.19, 1.17, 1.18)

#time.sleep(1)

#orders = api.orders()
#print(orders)
# for order in orders:
#     api.orderCancelById(order['ord_id'])

time.sleep(1)

#orders = api.orders()
#print(orders)

#positions = api.positions()
#print(positions)

position_buy = api.getPositionIdByClientId(clid_buy)
position_sell = api.getPositionIdByClientId(clid_sell)

print('buy gain ' + position_buy['gain'])
print('sell gain ' + position_sell['gain'])

api.close_all()
api.cancel_all()

# history = api.history("GBPUSD", "M5", int(datetime.now().timestamp()) - 10000)
# print(history)