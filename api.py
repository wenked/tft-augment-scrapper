from fastapi import FastAPI,status,HTTPException,BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import sqlite3
import logging
import subprocess
import pika
import time
import json
from random import randrange
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')
def callback(ch, method, properties, body):
    teste = eval(body)
    print(teste,'RECEIVER')
    print(" [x]xxxx Received %r" % body)
    time.sleep(randrange(0, 5))
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume('hello',callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()






logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


db = sqlite3.connect('augments.db')
cursor = db.cursor()

def execute_script():
    subprocess.call('main.py scrap',shell=True)
    
    


app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
    "https://hoppscotch.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

      


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/updatedb",status_code=status.HTTP_201_CREATED)
async def update_db(background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(execute_script)
        return {"message": "Database está sendo atualizada, aguarde um momento!"}
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail="Error ao fazer update da db")

@app.get("/augments",status_code=status.HTTP_200_OK)
async def get_augments():
    logging.info('Buscando augments...')
    try:
        augment_data = pd.read_sql(f'SELECT * FROM augments order by placement asc', db)
        formated_data = augment_data.to_dict(orient='records')
        logging.info('Buscando realizada com sucesso')
        return formated_data
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=404, detail="Error ao encontrar augments")