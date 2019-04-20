import requests
import os
from flask import request, jsonify, make_response
from app import app, db, mem

@app.route("/")
def main():
    return "Gateway Service"


if __name__ == "__main__":
    app.run(host="0.0.0.0")