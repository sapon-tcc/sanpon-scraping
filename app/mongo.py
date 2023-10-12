import os
import pymongo

class MongoDB():
    
    def __init__(self):
        
        self.client = pymongo.MongoClient(os.getenv("MONGODB_URL", "mongodb://localhost:27017/"))
        self.db = self.client["sapon"]
        self.colecao = self.db["opinioes"]
        
    def retrieve_books_to_scraping(self):
        self.colecao = self.db["books"]
        return self.colecao.find({"isGrated": False}).limit(10)
        