import requests
import os
from flask import request, jsonify, make_response
from app import app


if __name__ == "__main__":
    app.run(host="0.0.0.0")