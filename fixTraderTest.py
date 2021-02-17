import sys
sys.path.append('../') 
import time

from dotenv import load_dotenv

load_dotenv()

from fixTrader import FixTrader
from ejtrader_ct.service.client_service import ClientService

client_service = ClientService()
client = client_service.listAll()['5f08dee14bddaa41008e6eec']

fixTrader = FixTrader(client)
#accountInfo = fixTrader.accountInfo()
#print(accountInfo)
#print(accountInfo['broker'])
#print(accountInfo['balance'])

time.sleep(1)

fixTrader.buy("EURUSD", 0.01, 1.18, 1.19)
fixTrader.sell("EURUSD", 0.01, 1.19, 1.18)

'''
time.sleep(1)

positions = fixTrader.positions()
print(positions)
for position in positions:
    fixTrader.positionCloseById(position['pos_id'], position['amount'])
'''

time.sleep(1)

fixTrader.buyLimit("EURUSD", 0.01, 1.17, 1.19, 1.18)
fixTrader.sellLimit("EURUSD", 0.01, 1.23, 1.17, 1.22)
fixTrader.buyStop("EURUSD", 0.01, 1.20, 1.24, 1.22)
fixTrader.sellStop("EURUSD", 0.01, 1.19, 1.17, 1.18)

time.sleep(1)

'''
orders = fixTrader.orders()
print(orders)
for order in orders:
    fixTrader.orderCancelById(order['ord_id'])
'''
positions = fixTrader.positions()
print(positions)

fixTrader.close_all()
fixTrader.cancel_all()

#history = fixTrader.history("EURUSD", "M5", int(datetime.now().timestamp()) - 10000)
#print(history)