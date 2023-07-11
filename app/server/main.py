from fastapi import FastAPI

from database.database import Database



app = FastAPI()

@app.get("/pay/user_id={user_id}amount={amount}")
def pay_user(user_id:str,amount:str):
    data = Database()
    data.get_tokens(user_id,int(amount))
    print(user_id,amount)
    return 'Success'



@app.get("/accrue{user_id}{amount}")
def accrue_user(user_id,amount):
    return {"Hello": "World"}



@app.get("/take{user_id}{amount}")
def take_user(user_id,amount):
    return {"Hello": "World"}


@app.get("/pay{user}{user_to}{amount}")
def send_money(user,user_to,amount):
    return {"Hello": "World"}


@app.get("/balance{user_id}")
def get_balance(user_id):
    return {"Hello": "World"}