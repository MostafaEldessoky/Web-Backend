import time
from redis_om import get_redis_connection 

redis_streams = get_redis_connection(host="172.18.0.2",port=6379)
redis = get_redis_connection(host="172.18.0.4",port=6379)

try:
    redis_streams.xgroup_create(name="refund_event",groupname="payment_group",mkstream=True)
except:
    print("group exist")

while True:
    time.sleep(1)
    try:
        events = redis_streams.xreadgroup("payment_group","refund_event",{"refund_event":">"},None)
        print(events)
        if events != []:
            for event in events:
                redis.hset(":main.order:" + event[1][0][1]["pk"],"stutus","refund")
    except:
        print("error_payment")