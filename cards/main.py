# import os

# from flask import request, jsonify, make_response
# import jwt
# import requests

# from cards.app import app, db




# # Helper to generate standardized error responses.
# def error_response(code, msg):
#     return make_response(jsonify({"error": msg}), code)


# # Generic error response handler.
# @app.errorhandler(500)
# def exception():
#     return error_response(500, "Internal error")


# # Simple route to help identify service and monitor it's health.
# @app.route("/")
# def hello():
#     return "card service"


# if __name__ == "__main__":
#     # Database contents are wiped on every start.
#     db.drop_all()
#     db.create_all()
    
