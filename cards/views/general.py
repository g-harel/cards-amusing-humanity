from flask import Blueprint, jsonify, request, make_response
from  util.uuid_generator import UuidGenerator
from database import db

main = Blueprint('main', __name__, url_prefix='')


@main.route('/', methods=['GET'])
def get_main():
    return "Cards Service"