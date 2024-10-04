from fastapi import FastAPI 
from redis_om import get_redis_connection , HashModel

redis = get_redis_connection(host="172.18.0.3",port=6379)

class inventory(HashModel):
    name : str
    price : float
    quantity : int

    class Meta:
        database = redis

# 8080
app = FastAPI()


@app.post("/create_product")
async def create_product(item:inventory):
    return item.save()

@app.get("/get_product")
async def get_product(key:str):
    return inventory.get(key)

@app.get("/get_all_products")
async def get_all_products():
    keys = inventory.all_pks()
    products = []
    for key in keys:
        products.append(inventory.get(key))
    return products


