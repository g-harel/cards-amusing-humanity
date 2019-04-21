from flask import Flask, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from views import gateway

app = Flask(__name__)
app.register_blueprint(gateway.gate)

@app.route('/')
def main_route():
    return make_response(jsonify({"msg": "Gateway Service"}, 200))
