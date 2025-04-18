import redis
import json

r = redis.Redis(host='172.31.82.94', port=6379, db=0)


def send_to_queue(service, data):
    payload = json.dumps({
        "service": service,
        "data": data
    })
    r.rpush("task_queue", payload)
