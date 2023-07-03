from pymongo import MongoClient


class Database:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["test"]
        self.collection = self.db["test"]

    def get_tokens(self,id:str,count:int):
        res = self.collection.find_one({'id':id})
        if res == None:
            self.collection.insert_one({'money':count,'id':id})
        else:
            self.collection.update_one({'id':id}, {'$set':{'money':res['money']+count}})


    def send_tokens(self,id:str,count:int):
        res = self.collection.find_one({'id': id})
        if res == None:
            return False
        else:
            if res['money']-count < 0:
                return False
            self.collection.update_one({'id': id}, {'$set': {'money': res['money'] - count}})
            return True


    def  send_tokens_to_user(self,adress:str, to_adress:str,count:int):
        res = self.send_tokens(adress,count)
        if res:
            self.get_tokens(to_adress,count)


