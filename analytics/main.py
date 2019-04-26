import os

from flask import Flask, request, jsonify, make_response
import jwt
import requests

from persistence.records import RecordStore
from persistence.tokens import TokenStore

# Token expiry in minutes.
# Value is used to clear the token blacklist.
exp = 60 * int(float(os.getenv("TOKEN_TTL_HOURS", default=1)))

app = Flask(__name__)

tokens = TokenStore()
records = RecordStore(app)

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
    if tokens.get(token):
        return error_response(403, "Duplicate submission")

    # Decode the token's data without validating it.
    # Token is assumed to be valid since it was verified by the signing service.
    payload = jwt.decode(token, verify=False, algorithms=["HS256"])

    # Verify that token contains question data of the correct type.
    question = payload.get("question")
    if (not question) or (not type(question) is dict):
        return error_response(400, "Malformed token payload, missing 'question'")
    question_id = question.get("id")
    if (not question_id) or (not type(question_id) is str):
        return error_response(400, "Malformed token payload, missing question 'id'")

    # Verify that token contains answers data of the correct type.
    answers = payload.get("answers")
    if (not answers) or (not type(answers) is list):
        return error_response(400, "Malformed token payload, missing 'answers'")
    for answer in answers:
        id = answer.get("id")
        if (not id) or (not type(id) is str):
            return error_response(400, "Malformed token payload, missing answer 'id'")

    # Create database Records to store game result.
    for answer in answers:
        if answer["id"] != choice:
            records.add(question_id, choice, answer["id"])

    # Temporarily add game to blacklist until it expires (with a safety buffer).
    tokens.set(token, exp + 60, token)

    # Count records that agree with the choice.
    count_agree = records.count_agree(question_id, choice, answers)

    # Count records that disagree with the choice.
    count_disagree = records.count_disagree(question_id, choice, answers)

    # Respond with similarity.
    return jsonify({
        "similarity": count_agree / (count_agree + count_disagree)
    })


if __name__ == "__main__":
    # Database contents are wiped on every start.
    records.reset()
    app.run(host="0.0.0.0")
