from pymongo import MongoClient
import os

db = MongoClient(os.getenv("MONGODB_SERVER"), int(os.getenv("MONGODB_PORT")))
schema = db[os.getenv("MONGODB_DATABASE")]
clients_table = schema.Client
servers_table = schema.Server
ctrader_servers_table = schema.CtraderServer