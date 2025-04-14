import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)


def send_to_queue(service, data):
    payload = json.dumps({
        "service": service,
        "data": data
    })
    r.rpush("task_queue", payload)
