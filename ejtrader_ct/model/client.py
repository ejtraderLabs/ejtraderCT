class Client:

    def __init__(self, name: str, server: str, broker: str, login: str, password: str, currency: str, server_id: int):
        self.name = name
        self.server = server
        self.broker = broker
        self.login = login
        self.password = password
        self.currency = currency
        self.server_id = server_id
        self.fix_status = 0
        self.positions = []
        self.orders = []
