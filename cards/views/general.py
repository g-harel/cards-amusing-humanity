from flask import Blueprint, jsonify, request, make_response

main = Blueprint('main', __name__, url_prefix='')


@main.route('/', methods=['GET'])
def get_main():
    return "Cards Service"