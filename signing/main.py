from datetime import datetime, timedelta

from flask import Flask, request, jsonify, make_response
import jwt

# TODO from env
key = "abcde"
exp = timedelta(hours=1)

app = Flask(__name__)

def error_response(code, msg):
    return make_response(jsonify({"error": msg}), code)


@app.route("/sign", methods=["POST"])
def sign():
    body = request.get_json()
    if (not body):
        return error_response(400, "No data")

    payload = body.get("payload")
    if (not payload) or (not type(payload) is dict):
        return error_response(400, "Malformed data")

    payload["exp"] = int(datetime.timestamp(datetime.now() + exp))
    token = jwt.encode(payload, key, algorithm="HS256")
    return jsonify({"token": token.decode("utf-8")})


@app.route("/verify")
def verify():
    return "signing service"


if __name__ == "__main__":
    app.run()
