import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis

# Postgres config used to connect to analytics database.
POSTGRES = {
    "db": os.environ["POSTGRES_DB"],
    "user": os.environ["POSTGRES_USER"],
    "pass": os.environ["POSTGRES_PASSWORD"],
    "host": "cards-postgres",
    "port": "5432",
}

app = Flask(__name__)

# Configure app before handing over the instance to SQLAlchemy.
app.config["SQLALCHEMY_DATABASE_URI"] = \
    "postgresql://%(user)s:%(pass)s@%(host)s:%(port)s/%(db)s" % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a database "client".
db = SQLAlchemy(app)

# Create a redis client.
kv = redis.Redis(host="cards-redis", port=6379, db=0)
