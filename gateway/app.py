import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
mem = redis.Redis(host="gateway-redis", port=6379, db=0)