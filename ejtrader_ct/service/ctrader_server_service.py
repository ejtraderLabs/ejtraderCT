from database import ctrader_servers_table
from service.client_service import ClientService
from bson.objectid import ObjectId
import json

class CtraderServerService:

    def __init__(self):
        self.client_service = ClientService()

    def listAll(self):
        ctrader_servers = self.list(ctrader_servers_table.find())
        for id in ctrader_servers:
            ctrader_servers[id]['clients'] = self.client_service.listByServer(id)
        return ctrader_servers

    def listExcept(self, actual_list):
        id_list = []
        for id in actual_list:
            id_list.append(ObjectId(id))
        return self.list(ctrader_servers_table.find({ "_id": { "$nin": id_list }}))

    def listRemoved(self, actual_list):
        all_list = self.listAll()
        removed_list = actual_list.copy()
        for id in all_list:
            if id in removed_list:
                removed_list.pop(id)
        return removed_list

    def insert(self, server):
        server._id = str(ctrader_servers_table.insert(json.loads(json.dumps(server.__dict__))).inserted_id)

    def update(self, id, newvalues):
        ctrader_servers_table.update({'_id': ObjectId(id)}, { "$set": newvalues })
    
    def getById(self, id):
        server = ctrader_servers_table.find({ "_id": ObjectId(id) })
        if server != None:
            server['_id'] = str(server['_id'])
        return server
    
    def getByName(self, name):
        server = ctrader_servers_table.find({ "name": name })
        if server != None:
            server['_id'] = str(server['_id'])
        return server
    
    def clear(self):
        ctrader_servers_table.drop()

    def list(self, cursor):
        clist = list(cursor)
        for x in clist:
            x['_id'] = str(x['_id'])
        return { x['_id']: x for x in clist }