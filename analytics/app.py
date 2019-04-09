import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis

POSTGRES = {
    "db": os.environ["POSTGRES_DB"],
    "user": os.environ["POSTGRES_USER"],
    "pass": os.environ["POSTGRES_PASSWORD"],
    "host": "analytics-postgres",
    "port": "5432",
}

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = \
    "postgresql://%(user)s:%(pass)s@%(host)s:%(port)s/%(db)s" % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

kv = redis.Redis(host="analytics-redis", port=6379, db=0)
