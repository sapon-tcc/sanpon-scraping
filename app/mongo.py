import pymongo

class MongoDB():
    
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["sapon"]
        self.colecao = self.db["opinioes"]
        