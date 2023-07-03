from pymongo import MongoClient


class Database:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["test"]
        self.collection = self.db["test"]

    def get_tokens(self,address:str,count:int):
        res = self.collection.find_one({'id':address})
        if res == None:
            self.collection.insert_one({'money':count,'id':address})
        else:
            self.collection.update_one({'id':address}, {'$set':{'money':res['money']+count}})


    def send_tokens(self,address:str,count:int):
        res = self.collection.find_one({'id': address})
        if res == None:
            return False
        else:
            if res['money']-count < 0:
                return False
            self.collection.update_one({'id': address}, {'$set': {'money': res['money'] - count}})
            return True


    def  send_tokens_to_user(self,address:str, to_address:str,count:int):
        res = self.send_tokens(address,count)
        if res:
            self.get_tokens(to_address,count)


    def get_balance_by_id(self,address:str):
        res = self.collection.find_one({'id':address})
        return (lambda x: x['money'] if x else False)(res)




