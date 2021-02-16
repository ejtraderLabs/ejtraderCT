from database import clients_table
from bson.objectid import ObjectId
import json

class ClientService:

    def listAll(self):
        return self.list(clients_table.find())

    def listExcept(self, actual_client_list):
        id_list = []
        for id in actual_client_list:
            id_list.append(ObjectId(id))
        return self.list(clients_table.find({ "_id": { "$nin": id_list }}))

    def listRemoved(self, actual_client_list):
        all_clients = self.listAll()
        removed_clients = actual_client_list.copy()
        for id in all_clients:
            if id in removed_clients:
                removed_clients.pop(id)
        return removed_clients

    def listByServer(self, server_id):
        cursor_clients = clients_table.find({ "server_id": server_id })
        return self.list(cursor_clients)

    def insert(self, client):
        client._id = str(clients_table.insert(json.loads(json.dumps(client.__dict__))).inserted_id)

    def update(self, id, newvalues):
        clients_table.update({'_id': ObjectId(id)}, { "$set": newvalues })
    
    def getById(self, id):
        client = clients_table.find({ "_id": ObjectId(id) })
        if client != None:
            client['_id'] = str(client['_id'])
        return client
    
    def getByName(self, name):
        client = clients_table.find({ "name": name })
        if client != None:
            client['_id'] = str(client['_id'])
        return client
    
    def clear(self):
        clients_table.drop()

    def list(self, cursor):
        clist = list(cursor)
        for x in clist:
            x['_id'] = str(x['_id'])
        return { x['_id']: x for x in clist }