import sys
import time
import zmq
import logging
import threading

class Subscribe:

    def __init__(self, server, parse_command, getPositionIdByOriginId, getOrdersIdByOriginId, cancelOrdersByOriginId, servers, ctrader_servers):
        self.server = server
        self.servers = servers
        self.ctrader_servers = ctrader_servers
        self.parse_command = parse_command
        self.getPositionIdByOriginId = getPositionIdByOriginId
        self.getOrdersIdByOriginId = getOrdersIdByOriginId
        self.cancelOrdersByOriginId = cancelOrdersByOriginId
        # v_type buy = 0, sell = 1, buy limit = 2, sell limit = 3, buy stop = 4, sell stop = 5
        self.types = {
            '0': 'buy',
            '1': 'sell',
            '2': 'buy limit',
            '3': 'sell limit',
            '4': 'buy stop',
            '5': 'sell stop'
        }
        self.ctx = zmq.Context()
        self.s = self.ctx.socket(zmq.SUB)
        self.s.bind(self.server)
        self.s.setsockopt(zmq.SUBSCRIBE, b"")
        logging.info("Bind server: %s" % self.server)

    def connect(self):
        self.sub_thread = threading.Thread(target=self.qrec)
        self.sub_thread.start()

    def get_type(self, v_type):
        return self.types.get(v_type, "invalid v_type")
    
    def qrec(self):
        try:
            while True:
                [topic, contents] = self.s.recv_multipart()
                recvMsg = contents.decode("utf-8")
                topic_str = topic.decode()
                self.process_message(topic_str, recvMsg)

        except KeyboardInterrupt:
            self.s.close()
            self.ctx.term()
            pass
    
    def process_message(self, topic_str, recvMsg):
        message = recvMsg.split(" ")

        if topic_str[0:7] == "client_":
            client_id = topic_str[7:]
            self.parse_command(recvMsg, client_id)
            return

        if topic_str[0:14] == "ctraderServer_":
            ctraderServer_id = topic_str[14:]
            self.parse_command(recvMsg, ctraderServer_id)
            return

        if topic_str[0:7] == "server_":
            server_id = topic_str[7:]
            if server_id in self.servers:
                clients = self.servers[server_id]['clients']
                for client_id in clients:
                    self.parse_command(recvMsg, client_id)
            return

        order = message[1].split("|")
        server_id = topic_str

        clients = {}
        if server_id in self.servers:
            clients = self.servers[server_id]['clients']
        elif server_id in self.ctrader_servers:
            clients = self.ctrader_servers[server_id]['clients']
        
        if len(clients) == 0:
            logging.info("Servidor nao encontrado ou sem clientes: %s", server_id)
            return

        v_action = order[0]
        v_symbol = order[1]
        v_ticket = order[2]
        v_type = order[3]
        v_openprice = order[4]
        v_closeprice = order[5]
        v_lots = order[6]
        v_sl = order[7]
        v_tp = order[8]

        logging.info("Server: %s, Action: %s, Symbol: %s, Lots: %s, Ticket: %s", server_id, v_action, v_symbol, v_lots, v_ticket)

        otype = self.get_type(v_type)
        symbol = v_symbol[:6]
        size = int(float(v_lots) * 100000)

        command_by_client = {}
        for client_id in clients:
            command_by_client[client_id] = []
        
        if v_action == 'OPEN':
            if int(v_type) > 1:
                # abre ordem pendente
                command = '{0} {1} {2} {3} {4}'.format(otype, symbol, size, v_openprice, v_ticket)
                # adiciona comando para cada client do server
                for client_id in command_by_client:
                    command_by_client[client_id].append(command)
            else:
                # abre posicao a mercado
                command = '{0} {1} {2} {3}'.format(otype, symbol, size, v_ticket)
                # adiciona comando para cada client do server
                for client_id in command_by_client:
                    command_by_client[client_id].append(command)
        elif v_action in ['CLOSED', 'PCLOSED']:
            for client_id in command_by_client:
                if int(v_type) > 1:
                    # ORDEM
                    # cancela ordens pendentes
                    ticket_orders = self.getOrdersIdByOriginId(v_ticket, client_id)
                    self.cancelOrdersByOriginId(ticket_orders, client_id)
                else:
                    # POSICAO
                    # cancela ordens pendentes abertas de TP e SL
                    ticket_orders = self.getOrdersIdByOriginId(v_ticket, client_id)
                    self.cancelOrdersByOriginId(ticket_orders, client_id)
                    # verifica qual o ticket do client pelo ticket do server
                    ticket = self.getPositionIdByOriginId(v_ticket, client_id)
                    if ticket != None:
                        # fecha posicao aberta
                        command = "close " + ticket + " " + str(size)
                        # adiciona comando para cada client do server
                        command_by_client[client_id].append(command)
            
        elif v_action == 'MODIFY':
            for client_id in command_by_client:
                # POSICAO: verifica qual o ticket do client pelo ticket do server
                ticket = self.getPositionIdByOriginId(v_ticket, client_id)
                if ticket != None:
                    # cancela ordens pendentes abertas de TP e SL
                    ticket_orders = self.getOrdersIdByOriginId(v_ticket, client_id)
                    self.cancelOrdersByOriginId(ticket_orders, client_id)
                    if float(v_sl) > 0:
                        # cancela ordens pendentes abertas de TP e SL
                        ticket_orders = self.getOrdersIdByOriginId(v_ticket, client_id)
                        self.cancelOrdersByOriginId(ticket_orders, client_id)
                        # abre posicao pendente SL
                        otype = 'sell stop' if v_type == '0' else 'buy stop'
                        commandSL = '{0} {1} {2} {3} {4} {5}'.format(otype, symbol, size, v_sl, v_ticket, ticket)
                        # adiciona comando SL para cada client do server
                        command_by_client[client_id].append(commandSL)
                    if float(v_tp) > 0:
                        # cancela ordens pendentes abertas de TP e SL
                        ticket_orders = self.getOrdersIdByOriginId(v_ticket, client_id)
                        self.cancelOrdersByOriginId(ticket_orders, client_id)
                        # abre posicao pendente TP
                        otype = 'sell limit' if v_type == '0' else 'buy limit'
                        commandTP = '{0} {1} {2} {3} {4} {5}'.format(otype, symbol, size, v_tp, v_ticket, ticket)
                        # adiciona comando TP para cada client do server
                        command_by_client[client_id].append(commandTP)
                # ORDEM: verifica qual o ticket do client pelo ticket do server
                tickets = self.getOrdersIdByOriginId(v_ticket, client_id)
                if tickets != None and len(tickets) > 0:
                    # cancela ordens pendentes abertas
                    ticket_orders = self.getOrdersIdByOriginId(v_ticket, client_id)
                    self.cancelOrdersByOriginId(ticket_orders, client_id)
                    # abre ordem pendente
                    command = '{0} {1} {2} {3} {4}'.format(otype, symbol, size, v_openprice, v_ticket)
                    command_by_client[client_id].append(command)

        # executa lista de comandos de cada client
        for client_id in command_by_client:
            commands_to_exec = command_by_client[client_id]
            for c in commands_to_exec:
                self.parse_command(c, client_id)