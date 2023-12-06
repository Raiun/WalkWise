import datetime
import json
from fastapi import FastAPI
from db import test, unlocks_table, authorized_table
from bson.json_util import dumps
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    print(test)
    return {"cool": "guy"}

@app.get("/authorizedUsers")
def root():
    cursor = authorized_table.find({})
    return dumps(cursor)

@app.get("/allUnlocks")
def getAllUnlocks():
    cursor = unlocks_table.find({})
    return dumps(cursor)

@app.put("/addUnlock/{name}/{status}")
def addUnlock(name: str, status: str):
    current_timestamp = datetime.datetime.now()
    str_timestamp = current_timestamp.strftime("%m/%d/%Y T:%H:%M:%S")
    data = {"name": name, "date": str_timestamp, "status": status}
    put_data = jsonable_encoder(data)
    try:
        unlocks_table.insert_one(data)
        return dumps(put_data)
    except Exception as e:
        print(e)
    return e

@app.put("/updateAuthorizations/{name}")
def updateAuthorizations(name: str):
    try:
        user = authorized_table.find_one({"name": name})
        current_authorization = user["permitted"]
        result = authorized_table.update_one({"name": name},
            {'$set': {"permitted": not current_authorization}})
        if result.modified_count > 0:
            return authorized_table.find_one({"name": name})
        else:
            return "Failed to update authorization"
    except Exception as e:
        print(e)
    return e

'''
@app.get("/all")
def get_all():
    data = collection.find({})
    return dumps(list(data))
    '''