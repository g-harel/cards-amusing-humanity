from datetime import datetime, timedelta
import os

from flask import Flask, request, jsonify, make_response
import jwt

# Token expiry in seconds.
exp = 60 * 60 * int(float(os.getenv("TOKEN_TTL_HOURS")))
key = os.getenv("SECRET_KEY")

app = Flask(__name__)


# Helper to generate standardized error responses.
def error_response(code, msg):
    return make_response(jsonify({"error": msg}), code)


# Generic error response handler.
@app.errorhandler(500)
def exception():
    return error_response(500, "Internal error")


# Simple route to help identify service and monitor it's health.
@app.route("/")
def hello():
    return "signing service"


# Handler to sign payloads.
@app.route("/sign", methods=["POST"])
def sign():
    # Verify that request contains data.
    # Empty json object or incorrect "Content-Type" header will cause an error.
    body = request.get_json()
    if (not body):
        return error_response(400, "No data")

    # Verify that request contains payload data of the correct type.
    payload = body.get("payload")
    if (not payload) or (not type(payload) is dict):
        return error_response(400, "Malformed payload")

    # Token expiry time is set to configured value.
    payload["exp"] = datetime.timestamp(datetime.now()) + exp

    token = jwt.encode(payload, key, algorithm="HS256")
    return jsonify({"token": token.decode("utf-8")})


@app.route("/verify", methods=["POST"])
def verify():
    # Verify that request contains data.
    # Empty json object or incorrect "Content-Type" header will cause an error.
    body = request.get_json()
    if (not body):
        return error_response(400, "No data")

    # Verify that request contains token data of the correct type.
    token = body.get("token")
    if (not token) or (not type(token) is str):
        return error_response(400, "Malformed body, missing 'token")

    try:
        # Decode the token and verify it's integrity using the secret key.
        jwt.decode(token, key, algorithms=["HS256"])
        return "Valid token"
    except:
        return error_response(401, "Expired or malformed token")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
