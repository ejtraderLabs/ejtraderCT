from database import servers_table
from service.client_service import ClientService
from bson.objectid import ObjectId
import json

class ServerService:

    def __init__(self):
        self.client_service = ClientService()

    def listAll(self):
        servers = self.list(servers_table.find())
        for id in servers:
            servers[id]['clients'] = self.client_service.listByServer(id)
        return servers

    def insert(self, server):
        server._id = str(servers_table.insert(json.loads(json.dumps(server.__dict__))).inserted_id)

    def getById(self, id):
        server = servers_table.find({ "_id": ObjectId(id) })
        if server != None:
            server['_id'] = str(server['_id'])
            server['clients'] = self.client_service.listByServer(server['_id'])
        return server
    
    def getByName(self, name):
        server = servers_table.find({ "name": name })
        if server != None:
            server['_id'] = str(server['_id'])
            server['clients'] = self.client_service.listByServer(server['_id'])
        return server
    
    def clear(self):
        servers_table.drop()
    
    def list(self, cursor):
        clist = list(cursor)
        for x in clist:
            x['_id'] = str(x['_id'])
        return { x['_id']: x for x in clist }