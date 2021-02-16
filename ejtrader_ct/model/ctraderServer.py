class CtraderServer:

    def __init__(self, name: str, clients = None, server: str, broker: str, login: str, password: str, currency: str):
        self.name = name
        self.clients = clients
        self.server = server
        self.broker = broker
        self.login = login
        self.password = password
        self.currency = currency
        self.fix_status = 0
        self.positions = []
        self.orders = []
