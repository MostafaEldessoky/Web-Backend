import time
from redis_om import get_redis_connection 

redis_streams = get_redis_connection(host="172.18.0.2",port=6379)
redis = get_redis_connection(host="172.18.0.3",port=6379)

try:
    redis_streams.xgroup_create("complete_event","inventory_group",mkstream=True)
except:
    print("group exist")

while True:
    time.sleep(1)
    try:
        events = redis_streams.xreadgroup("inventory_group","complete_event",{"complete_event":">"},None)
        print(events)
        if events !=[]:
            for event in events:
                quantity = redis.hget(":main.inventory:" + event[1][0][1]["product_id"],"quantity")
                quantity = int(quantity) - int(event[1][0][1]["quantity"])
                if quantity < 0:
                    redis_streams.xadd("refund_event",event[1][0][1],"*")
                else:
                    redis.hset(":main.inventory:" + event[1][0][1]["product_id"],"quantity",quantity)
    except:
        print("error_inventory")
    