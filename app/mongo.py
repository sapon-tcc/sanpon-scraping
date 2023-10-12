import os
import pymongo

class MongoDB():
    
    def __init__(self, db):
        
        self.client = pymongo.MongoClient(os.getenv("MONGODB_URL", "mongodb://localhost:27017/"))
        self.db = self.client["sapon"]
        self.colecao = self.db[db]
        
    def retrieve_books_to_scraping(self):
        return self.colecao.find({"isGrated": False}).limit(10)
    
    def update_book(self, book):
        atualizacao = {
            "$set": {
                "isGrated": True
            }
        }
        return self.colecao.update_one({"_id": book["_id"]}, atualizacao)
        