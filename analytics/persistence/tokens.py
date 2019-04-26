import redis

class TokenStore():
    # Create a redis client.
    kv = None

    def __init__(self):
        self.kv = redis.Redis(host="analytics-redis", port=6379, db=0)

    def get(self, key):
        return self.kv.get(key)

    def set(self, key, exp, val):
        return self.kv.setex(key, exp, val)
