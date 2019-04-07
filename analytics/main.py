from flask import request, jsonify, make_response
import jwt
import requests

from app import app, db


def error_response(code, msg):
    return make_response(jsonify({"error": msg}), code)


@app.errorhandler(500)
def exception():
    return error_response(500, "Internal error")


@app.route("/")
def hello():
    return "analytics service"


@app.route("/submit", methods=["POST"])
def submit():
    body = request.get_json()
    if (not body):
        return error_response(400, "No data")

    token = body.get("token")
    if (not token) or (not type(token) is str):
        return error_response(400, "Malformed body, missing 'token'")

    choice = body.get("choice")
    if (not choice) or (not type(choice) is str):
        return error_response(400, "Malformed body, missing 'choice'")

    res = requests.post("http://signing/verify", json={"token":token})
    if (res.status_code == 400) or (res.status_code == 500):
        return error_response(500, "Internal error")
    elif (res.status_code == 401):
        return error_response(401, "Expired or malformed token")

    try:
        token = jwt.decode(token, verify=False, algorithms=["HS256"])
    except:
        return error_response(401, "Malformed token")

    return jsonify(token)


if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    app.run(host="0.0.0.0")
