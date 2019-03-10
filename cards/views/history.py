from flask import Blueprint, jsonify
from domain.models.history import History,  row2dict
from datasource.database import db


his = Blueprint('history', __name__, url_prefix='/api')


@his.route('/history', methods=['GET'])
def get_all_answers():
    answers_list = History.query.all()
    db.session.close()
    return jsonify([row2dict(answer) for answer in answers_list])
