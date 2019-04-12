from flask import Blueprint, jsonify, request, make_response
from  util.uuid_generator import UuidGenerator
from models.answers import Answer, row2dict
from database import db

ans = Blueprint('answers', __name__, url_prefix='/api')


@ans.route('/answers', methods=['GET'])
def get_all_answers():
    try:
        answers_list = Answer.query.all()
        db.session.close()
        return jsonify([row2dict(answer) for answer in answers_list])
    except:
        print("Problem while getting all answers")
        return make_response(jsonify({"code": 404, "msg": "Can't process request"}), 404)


@ans.route('/answers/<answer_id>', methods=['GET'])
def get_answer(answer_id):
    if not answer_id:
        return make_response(jsonify({"code": 412, "msg": "Precondition Failed"}, 412))
    answer = None
    try:
        answer = Answer.query.filter_by(id=answer_id).first()
        if answer is None:
            return make_response(jsonify({"code": 404, "msg": "Doesn't exists"}), 404)

        db.session.close()
        return jsonify([row2dict(answer)])
    except:
        print("Problem while getting an answer")
        return make_response(jsonify({"code": 404, "msg": "Can't process request"}), 404)
    finally:
        db.session.close()

