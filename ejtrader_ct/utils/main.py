import logging
import re
import threading
import time
import os
from decimal import Decimal
from operator import itemgetter
from fix import FIX, Side, OrderType
from subscribe import Subscribe
from model.client import Client
from model.server import Server
import json
from service.server_service import ServerService
from service.ctrader_server_service import CtraderServerService
from service.client_service import ClientService
from dotenv import load_dotenv

load_dotenv()

class Main:

    def __init__(self):
        self.server_service = ServerService()
        self.ctrader_server_service = CtraderServerService()
        self.client_service = ClientService()
        self.servers = self.server_service.listAll()
        self.ctrader_servers = self.ctrader_server_service.listAll()
        self.clients = self.client_service.listAll()
        self.update_trades_interval = 10
        self.update_trades_thread = threading.Thread(target=self.update_trades)
        self.update_trades_thread.start()
        self.market_data_list = {}
        self.subscribe = Subscribe(os.getenv("COMMAND_ADDRESS_SUBSCRIBE"), self.parse_command, self.getPositionIdByOriginId, self.getOrdersIdByOriginId, self.cancelOrdersByOriginId, self.servers, self.ctrader_servers)

    def run(self):
        logging.getLogger().setLevel(logging.INFO)

        # inicia subscribe para receber ordens via zmq
        self.subscribe.connect()

        for id in self.clients:
            c = self.clients[id]
            c['fix'] = FIX(c['server'], c['broker'], c['login'], c['password'], c['currency'], c['_id'], self.position_list_callback, self.order_list_callback, self.update_fix_status_client, False, self.subscribe)
        
        for id in self.ctrader_servers:
            c = self.ctrader_servers[id]
            c['fix'] = FIX(c['server'], c['broker'], c['login'], c['password'], c['currency'], c['_id'], self.ctrader_position_list_callback, self.ctrader_order_list_callback, self.update_fix_status_ctrader_server, True, self.subscribe)

    def parse_command(self, command: str, client_id: str):
        parts = command.split(" ")
        logging.debug(parts)
        logging.info("Command: %s - client_id: %s", command, client_id)

        if client_id not in self.clients:
            logging.info("client_id not found: %s", client_id)
            return
        
        fix = self.clients[client_id]['fix']

        if fix.logged == False:
            logging.info("waiting logging...")
            return

        if parts[0] == "sub":
            try:
                subid = int(parts[1])
                fix.market_request(subid - 1, parts[2].upper(), self.quote_callback)
            except ValueError:
                logging.error("Invalid subscription ID")
        if parts[0] in ["buy", "sell"]:
            if parts[1] in ["stop", "limit"]:
                fix.new_limit_order(
                    parts[2].upper(),
                    Side.Buy if parts[0] == "buy" else Side.Sell,
                    OrderType.Limit if parts[1] == "limit" else OrderType.Stop,
                    float(parts[3]),
                    float(parts[4]),
                    parts[5] if len(parts) >= 6 else None,
                    parts[6] if len(parts) >= 7 else None
                )
            else:
                fix.new_market_order(
                    parts[1].upper(),
                    Side.Buy if parts[0] == "buy" else Side.Sell,
                    float(parts[2]),
                    parts[3] if len(parts) >= 4 else None,
                    parts[4] if len(parts) >= 5 else None
                )
        if parts[0] == "close":
            if parts[1] == "all":
                fix.close_all()
            else:
                if len(parts) == 3:
                    fix.close_position(parts[1], parts[2])
                else:
                    fix.close_position(parts[1])
        if parts[0] == "cancel":
            if parts[1] == "all":
                fix.cancel_all()
            else:
                fix.cancel_order(parts[1])

    def float_format(self, fmt: str, num: float, force_sign = True):
        return max(('{:+}' if force_sign else "{}").format(round(num, 6)), fmt.format(num), key=len)

    def position_list_callback(self, data: dict, price_data: dict, client_id: str):
        positions = []
        for i, kv in enumerate(data.items()):
            pos_id = kv[0]
            name = kv[1]["name"]
            side = "Buy" if kv[1]["long"] > 0 else "Sell"
            amount = kv[1]["long"] if kv[1]["long"] > 0 else kv[1]["short"]
            price_str = self.float_format("{:.%df}" % kv[1]["digits"], kv[1]["price"], False)
            price = price_data.get(name, None)
            actual_price = ""
            diff_str = ""
            pl_str = ""
            gain_str = ""
            if price:
                if side == "Buy":
                    p = price["bid"]
                else:
                    p = price["offer"]
                actual_price = ("{:.%df}" % kv[1]["digits"]).format(p)
                diff = p - kv[1]["price"]
                if side == "Sell":
                    diff = -diff
                diff_str = self.float_format("{:+.%df}" % kv[1]["digits"], diff)
                pl = amount * diff
                pl_str = self.float_format("{:+.2f}", pl)
                convert = kv[1]["convert"]
                convert_dir = kv[1]["convert_dir"]
                price = price_data.get(convert, None)
                if price:
                    if convert_dir:
                        rate = 1 / price["offer"]
                    else:
                        rate = price["bid"]
                    pl_base = pl * rate
                    gain_str = "{:+.2f}".format(round(pl_base, 2))
            # adiciona informacoes de posicoes no client
            positions.append({
                "pos_id" : pos_id,
                "name" : name,
                "side" : side,
                "amount" : amount,
                "price" : price_str,
                "actual_price" : actual_price,
                "diff" : diff_str,
                "pl" : pl_str,
                "gain" : gain_str
            })
        self.clients[client_id].update(positions = positions)
        logging.debug("client_id %s positions: %s", client_id, positions)

    def getPositionIdByOriginId(self, posId: str, client_id: str):
        client = self.clients[client_id]
        if "fix" in client and posId in client['fix'].origin_to_pos_id:
            return client['fix'].origin_to_pos_id[posId]
        return None

    def getOrdersIdByOriginId(self, ordId: str, client_id: str):
        client = self.clients[client_id]
        if "fix" in client and ordId in client['fix'].origin_to_ord_id:
            return client['fix'].origin_to_ord_id[ordId]
        return None

    def cancelOrdersByOriginId(self, clIdArr, client_id: str):
        if clIdArr == None:
            return
        client = self.clients[client_id]
        if "fix" in client:
            for clId in clIdArr:
                client['fix'].cancel_order(clId)

    def order_list_callback(self, data: dict, price_data: dict, client_id: str):
        orders = []
        for i, kv in enumerate(data.items()):
            ord_id = kv[0]
            name = kv[1]["name"]
            side = "Buy" if kv[1]["side"] == Side.Buy else "Sell"
            amount_str = str(kv[1]["amount"])
            order_type = kv[1]["type"]
            price_str = ""
            if order_type > 1:
                price_str = self.float_format("{:.%df}" % kv[1]["digits"], kv[1]["price"], False)
            price = price_data.get(name, None)
            actual_price = ""
            if price:
                if side == "Buy":
                    price = price["offer"]
                else:
                    price = price["bid"]
                actual_price = self.float_format("{:.%df}" % kv[1]["digits"], price, False)
            pos_id = kv[1]["pos_id"]
            # adiciona informacoes de ordens no client
            orders.append({
                "ord_id" : ord_id,
                "name" : name,
                "side" : side,
                "amount" : amount_str,
                "price" : price_str,
                "actual_price" : actual_price,
                "pos_id" : pos_id,
                "clid" : kv[1]["clid"]
            })
        self.clients[client_id].update(orders = orders)
        logging.debug("client_id %s orders: %s", client_id, orders)

    def quote_callback(self, name: str, digits: int, data: dict):
        if len(data) == 0:
            return
        offer = []
        bid = []
        for e in data.values():
            if e["type"] == 0:
                bid.append(e)
            else:
                offer.append(e)
        offer.sort(key=itemgetter("price"))
        bid.sort(key=itemgetter("price"), reverse=True)
        for i, e in enumerate(bid):
            p = ("{:.%df}" % digits).format(e["price"])
            if "size" in e.keys():
                a = str(e["size"])
        for i, e in enumerate(offer):
            p = ("{:.%df}" % digits).format(e["price"])
            if "size" in e.keys():
                a = str(e["size"])
        bid_str = ("{:.%df}" % digits).format(bid[0]["price"])
        offer_str = ("{:.%df}" % digits).format(offer[0]["price"])
        spread_str = ("{:.%df}" % digits).format(offer[0]["price"] - bid[0]["price"])
        self.market_data_list[name] = { "bid": bid_str, "ask": offer_str, "spread": spread_str, "time": time.time()}
    
    def update_trades(self):
        while True:
            # faz logout de clients removidos
            removed_clients = self.client_service.listRemoved(self.clients)
            for id in removed_clients:
                if 'fix' in removed_clients[id]:
                    removed_clients[id]['fix'].logout()
                    self.clients.pop(id)
            # verifica se existem novos clients no banco
            new_clients = self.client_service.listExcept(self.clients)
            if new_clients:
                for id in new_clients:
                    c = new_clients[id]
                    c['fix'] = FIX(c['server'], c['broker'], c['login'], c['password'], c['currency'], c['_id'], self.position_list_callback, self.order_list_callback, self.update_fix_status_client, False, self.subscribe)
                    self.clients[id] = c
            # atualiza fix_status, lista de positions e orders de cada client
            for id in self.clients:
                client = self.clients[id]
                fix_status = 1 if 'fix' in client and client['fix'].logged else 0
                newvalues = { 'fix_status': fix_status }
                if 'positions' in client:
                    newvalues.update(positions = client['positions'])
                if 'orders' in client:
                    newvalues.update(orders = client['orders'])
                self.client_service.update(id, newvalues)
                if "fix" in client:
                    if len(client['positions']) == 0:
                        client['fix'].origin_to_pos_id = {}
                    if len(client['orders']) == 0:
                        client['fix'].origin_to_ord_id = {}
            # faz logout de ctrader_servers removidos
            removed_ctrader_servers = self.ctrader_server_service.listRemoved(self.ctrader_servers)
            for id in removed_ctrader_servers:
                if 'fix' in removed_ctrader_servers[id]:
                    removed_ctrader_servers[id]['fix'].logout()
                    self.ctrader_servers.pop(id)
            # verifica se existem novos ctrader_servers no banco
            new_ctrader_servers = self.ctrader_server_service.listExcept(self.ctrader_servers)
            if new_ctrader_servers:
                for id in new_ctrader_servers:
                    c = new_ctrader_servers[id]
                    c['fix'] = FIX(c['server'], c['broker'], c['login'], c['password'], c['currency'], c['_id'], self.position_list_callback, self.order_list_callback, self.update_fix_status_ctrader_server, True, self.subscribe)
                    self.ctrader_servers[id] = c
            # atualiza fix_status, lista de positions e orders de cada ctrader_server
            for id in self.ctrader_servers:
                ctrader_server = self.ctrader_servers[id]
                fix_status = 1 if 'fix' in ctrader_server and ctrader_server['fix'].logged else 0
                newvalues = { 'fix_status': fix_status }
                if 'positions' in ctrader_server:
                    newvalues.update(positions = ctrader_server['positions'])
                if 'orders' in ctrader_server:
                    newvalues.update(orders = ctrader_server['orders'])
                self.ctrader_server_service.update(id, newvalues)
                if "fix" in ctrader_server:
                    if len(ctrader_server['positions']) == 0:
                        ctrader_server['fix'].origin_to_pos_id = {}
                    if len(ctrader_server['orders']) == 0:
                        ctrader_server['fix'].origin_to_ord_id = {}
            time.sleep(self.update_trades_interval)

    def update_fix_status_client(self, client_id, logged):
        self.client_service.update(client_id, { 'fix_status': 1 if logged else 0 })

    def update_fix_status_ctrader_server(self, server_id, logged):
        self.ctrader_server_service.update(server_id, { 'fix_status': 1 if logged else 0 })
    
    def ctrader_position_list_callback(self, data: dict, price_data: dict, server_id: str):
        positions = []
        for i, kv in enumerate(data.items()):
            pos_id = kv[0]
            name = kv[1]["name"]
            side = "Buy" if kv[1]["long"] > 0 else "Sell"
            amount = kv[1]["long"] if kv[1]["long"] > 0 else kv[1]["short"]
            price_str = self.float_format("{:.%df}" % kv[1]["digits"], kv[1]["price"], False)
            price = price_data.get(name, None)
            actual_price = ""
            diff_str = ""
            pl_str = ""
            gain_str = ""
            if price:
                if side == "Buy":
                    p = price["bid"]
                else:
                    p = price["offer"]
                actual_price = ("{:.%df}" % kv[1]["digits"]).format(p)
                diff = p - kv[1]["price"]
                if side == "Sell":
                    diff = -diff
                diff_str = self.float_format("{:+.%df}" % kv[1]["digits"], diff)
                pl = amount * diff
                pl_str = self.float_format("{:+.2f}", pl)
                convert = kv[1]["convert"]
                convert_dir = kv[1]["convert_dir"]
                price = price_data.get(convert, None)
                if price:
                    if convert_dir:
                        rate = 1 / price["offer"]
                    else:
                        rate = price["bid"]
                    pl_base = pl * rate
                    gain_str = "{:+.2f}".format(round(pl_base, 2))
            # adiciona informacoes de posicoes no client
            positions.append({
                "pos_id" : pos_id,
                "name" : name,
                "side" : side,
                "amount" : amount,
                "price" : price_str,
                "actual_price" : actual_price,
                "diff" : diff_str,
                "pl" : pl_str,
                "gain" : gain_str
            })
        self.ctrader_servers[server_id].update(positions = positions)
        logging.info("ctrader server_id %s positions: %s", server_id, positions)
    
    def ctrader_order_list_callback(self, data: dict, price_data: dict, server_id: str):
        orders = []
        for i, kv in enumerate(data.items()):
            ord_id = kv[0]
            name = kv[1]["name"]
            side = "Buy" if kv[1]["side"] == Side.Buy else "Sell"
            amount_str = str(kv[1]["amount"])
            order_type = kv[1]["type"]
            price_str = ""
            if order_type > 1:
                price_str = self.float_format("{:.%df}" % kv[1]["digits"], kv[1]["price"], False)
            price = price_data.get(name, None)
            actual_price = ""
            if price:
                if side == "Buy":
                    price = price["offer"]
                else:
                    price = price["bid"]
                actual_price = self.float_format("{:.%df}" % kv[1]["digits"], price, False)
            pos_id = kv[1]["pos_id"]
            # adiciona informacoes de ordens no client
            orders.append({
                "ord_id" : ord_id,
                "name" : name,
                "side" : side,
                "amount" : amount_str,
                "price" : price_str,
                "actual_price" : actual_price,
                "pos_id" : pos_id,
                "clid" : kv[1]["clid"]
            })
        self.ctrader_servers[server_id].update(orders = orders)
        logging.info("ctrader server_id %s orders: %s", server_id, orders)

logging.addLevelName(logging.WARNING, "\033[91m%s\033[0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName(logging.ERROR, "\033[101m%s\033[0m" % logging.getLevelName(logging.ERROR))
main = Main()
main.run()