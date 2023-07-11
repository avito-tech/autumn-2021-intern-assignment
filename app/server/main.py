from fastapi import FastAPI

from database.database import Database



app = FastAPI()

@app.get("/pay/user_id={user_id}amount={amount}")
def pay_user(user_id:str,amount:str):
    data = Database()
    try:
        data.send_tokens(user_id,int(amount))
        return {'Success':True}
    except:
        return {'Success':False}

@app.get("/accrue/user_id={user_id}amount={amount}")
def accrue_user(user_id:str,amount:str):
    data = Database()
    try:
        data.get_tokens(user_id, int(amount))
        return {'Success':True}
    except:
        return {'Success':False}

@app.get("/pay/user={user}user_to={user_to}amount={amount}")
def send_money(user,user_to,amount):
    data = Database()
    try:
        res = data.send_tokens_to_user(user,user_to,int(amount))
        if res:
            return {'Success':True}
        else:
            return {'Success':False}
    except:
        return {'Success':False}

@app.get("/balance/user_id={user_id}")
def get_balance(user_id:str):
    data = Database()
    res = data.get_balance_by_id(user_id)
    print(user_id,res)
    if res:
        return {'Success':True,'result':{'user_id':user_id,'balance':res}}
    else:
        return {'Success':False}