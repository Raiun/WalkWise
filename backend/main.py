import datetime
from fastapi import FastAPI
from db import test, collection
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

@app.put("/addUnlock")
def addUnlock():
    current_timestamp = datetime.datetime.now()
    data = {"name": "", "date": current_timestamp, "status": ""}
    put_data = jsonable_encoder(data)
    print(data)
    print(put_data)
    try:
        #collection.insert_one()
        return 1
    except Exception as e:
        print(e)
    return -1

'''
@app.get("/all")
def get_all():
    data = collection.find({})
    return dumps(list(data))
    '''