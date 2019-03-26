from datetime import datetime, timedelta
import os

from flask import Flask, request, jsonify, make_response
import jwt

key = os.getenv("SECRET_KEY")
exp = int(float(os.getenv("TOKEN_TTL_HOURS")))

app = Flask(__name__)


def error_response(code, msg):
    return make_response(jsonify({"error": msg}), code)


@app.errorhandler(500)
def exception():
    return error_response(500, "Internal error")


@app.route("/sign", methods=["POST"])
def sign():
    body = request.get_json()
    if (not body):
        return error_response(400, "No data")

    payload = body.get("payload")
    if (not payload) or (not type(payload) is dict):
        return error_response(400, "Malformed payload")

    payload["exp"] = int(datetime.timestamp(datetime.now() + exp))
    token = jwt.encode(payload, key, algorithm="HS256")
    return jsonify({"token": token.decode("utf-8")})


@app.route("/verify", methods=["POST"])
def verify():
    body = request.get_json()
    if (not body):
        return error_response(400, "No data")

    token = body.get("token")
    if (not token) or (not type(token) is str):
        return error_response(400, "Malformed token")

    try:
        jwt.decode(token, key, algorithms=['HS256'])
        return "Valid token"
    except:
        return error_response(401, "Expired or malformed token")


if __name__ == "__main__":
    app.run()
