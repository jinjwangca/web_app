from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import json
import pymongo
import logging
logging.basicConfig(level=logging.DEBUG)


class DatabaseGateway:
    def __init__(self):
        self.db = self.setup_db()

    def ping(self):
        uri = os.getenv("MONGODBURI", "")
        print(uri)
        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))
        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            logging(e)
            print(e)

    def setup_db(self):
        uri = os.getenv("MONGODBURI", "")
        self.ping()
        client =  MongoClient(uri, server_api=ServerApi('1'))
        mongo_db = client.StockAnalysis

        return mongo_db

    def add_data(self, id, data, collection_name):
        try:
            dbcollection = self.db[collection_name]
            x=dbcollection.insert_one({"_id": id, "data":data}).inserted_id
        except Exception as e:
            return None
        return x

    def delete_data(self, id, collection_name):
        try:
            dbcollection = self.db[collection_name]
            return dbcollection.delete_one({"_id": id}).deleted_count
        except Exception as e:
            return None

    def delete_all_data(self, collection_name):
        try:
            dbcollection = self.db[collection_name]
            return dbcollection.delete_many({}).deleted_count
        except Exception as e:
            return None

    def get_data(self, id, collection_name):
        try:
            dbcollection = self.db[collection_name]
            return dbcollection.find_one({"_id":id})['data']
        except Exception as e:
            print(e)
            return None

    def get_all_data(self, collection_name):
        try:
            dbcollection = self.db[collection_name]
            return list(dbcollection.find())
        except Exception as e:
            return None


# Main function
# if __name__ == "__main__":
#     gateway = DatabaseGateway()
#     gateway.add_data(1,'test','TradeInfo')
#     print(gateway.get_all_data('TradeInfo'))