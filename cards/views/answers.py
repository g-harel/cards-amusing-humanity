from flask import Blueprint, jsonify, request, make_response
from domain.models.answer import Answer,  row2dict
from util.uuid_generator import UuidGenerator
from datasource.database import db


ans = Blueprint('answers', __name__, url_prefix='/api')


@ans.route('/answers', methods=['GET'])
def get_all_answers():
    answers_list = Answer.query.all()
    db.session.close()
    return jsonify([row2dict(answer) for answer in answers_list])


@ans.route('/answers/<answer_id>', methods=['GET'])
def get_answer(answer_id):
    if not answer_id:
        return make_response(jsonify({"code": 412, "msg": "Precondition Failed"}, 412))
    answer = None
    try:
        answer = Answer.query.filter_by(id=answer_id).first()
        if answer is None:
            return make_response(jsonify({"code": 404, "msg": "Doesn't exists"}), 404)
    except Exception as error:
        print("Problem while getting an answer")
        print(error)
        db.session.rollback()
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    finally:
        db.session.close()
        return jsonify([row2dict(answer)])
