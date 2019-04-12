import os

from flask import request, jsonify, make_response
import jwt
import requests

from app import app, db, kv
from models import Record

# Token expiry in minutes.
# Value is used to clear the token blacklist.
exp = 60 * int(float(os.getenv("TOKEN_TTL_HOURS")))


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
    return "analytics service"


# Handler for completed games.
@app.route("/submit", methods=["POST"])
def submit():
    # Verify that request contains data.
    # Empty json object or incorrect "Content-Type" header will cause an error.
    body = request.get_json()
    if (not body):
        return error_response(400, "No data")

    # Verify that request contains token data of the correct type.
    token = body.get("token")
    if (not token) or (not type(token) is str):
        return error_response(400, "Malformed body, missing 'token'")

    # Verify that request contains choice data of the correct type.
    choice = body.get("choice")
    if (not choice) or (not type(choice) is str):
        return error_response(400, "Malformed body, missing 'choice'")

    # Check with the signing service that the token is valid.
    res = requests.post("http://signing/verify", json={"token":token})
    if (res.status_code == 401):
        return error_response(401, "Expired or malformed token")
    elif (res.status_code != 200):
        return error_response(500, "Internal error")

    # Check blacklist to see if game has already been submitted.
    if kv.get(token):
        return error_response(403, "Duplicate submission")

    # Decode the token's data without validating it.
    # Token is assumed to be valid since it was verified by the signing service.
    payload = jwt.decode(token, verify=False, algorithms=["HS256"])

    # Create database Records to store game result.
    rows = []
    for answer in payload["answers"]:
        if answer["id"] != choice:
            rows.append(Record( question=payload["question"], selected_answer=choice, other_answer=answer["id"]))

    # Bulk insert new rows into the database.
    db.session.bulk_save_objects(rows)
    db.session.commit()

    # Temporarily add game to blacklist until it expires (with a safety buffer).
    kv.setex(token, exp + 60, token)

    return jsonify(payload)


if __name__ == "__main__":
    # Database contents are wiped on every start.
    db.drop_all()
    db.create_all()
    app.run(host="0.0.0.0")
