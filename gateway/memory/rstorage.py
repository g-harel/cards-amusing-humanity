import redis
from memory.storage import Storage
import logging

# Instance of the in-memory-database
memdb = redis.Redis(host="gateway-redis", port=6379, db=0)
gunicorn_logger = logging.getLogger('gunicorn.error')


class RedisStorage(Storage):

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def get(self, key):
        """ Get data using key """
        data = None
        try:
            super().get(self, key)
            gunicorn_logger.info(key)
            ip = str(key)
            data = memdb.hmget(ip, ['ip', 'counter', 'last_transaction'])
        except Exception as error:
            gunicorn_logger.error(error)
        
        return data

    def set(self, key, data):
        """ Set Data  """
        try:
            super().set(self, key, data)
            ip = str(key)
            memdb.hmset(ip, {'ip': data['ip'], 'counter': data['counter'],'last_transaction': data['last_transaction']})
        except Exception as error:
            gunicorn_logger.error(error)

    def exists(self, key):
        """ Exists  """
        exist = False
        try:
            exist = memdb.exists(key)
        except Exception as error:
            gunicorn_logger.error(error)

        return exist
