from flask import Blueprint, jsonify, make_response

main = Blueprint('main', __name__, url_prefix='/')


@main.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"code": 404, "msg": "404: Not Found"}), 404)


@main.route('/')
def soen487_a1():
    return jsonify({"title": "Card Services"})
