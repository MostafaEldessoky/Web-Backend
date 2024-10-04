from fastapi import FastAPI 
from redis_om import get_redis_connection , HashModel
import requests
import time
from fastapi.background import BackgroundTasks
import time

redis_streams = get_redis_connection(host="172.18.0.2",port=6379)
redis = get_redis_connection(host="172.18.0.4",port=6379)

class order(HashModel):
    product_id : str
    name : str
    price : float
    quantity : int
    total_price : float 
    stutus : str 

    class Meta:
        database = redis


# 6060
app = FastAPI()

@app.get("/get_order")
async def get_order(key : str):
    return order.get(key)

@app.post("/buy_product")
async def buy_product(key: str, quantityy : int , BackgroundTasks : BackgroundTasks):
    product = requests.get(url = "http://172.18.0.5:8000/get_product", params={"key":key}).json()
    my_order = order(product_id = product["pk"], name = product["name"],price = product["price"],quantity =  quantityy, total_price = quantityy * product["price"],stutus = "pending")
    my_order.save()
    BackgroundTasks.add_task(payment,my_order)
    return my_order

def payment(order : order):
    time.sleep(10)
    order.stutus = "completed"
    order.save()
    redis_streams.xadd("complete_event",order.model_dump(),"*")

