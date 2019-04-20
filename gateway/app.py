from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from views import gateway

app = Flask(__name__)
app.register_blueprint(gateway.gate)
