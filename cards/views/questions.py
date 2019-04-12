from flask import Blueprint, jsonify, request, make_response
from  util.uuid_generator import UuidGenerator
from models.questions import Question, row2dict
from database import db

questions = Blueprint('questions', __name__, url_prefix='/api')


@questions.route('/questions', methods=['GET'])
def get_all_questions():
    try:
        question_list = Question.query.all()
        db.session.close()
        return jsonify([row2dict(q) for q in question_list])
    except:
        print("Problem while getting all questions")
        return make_response(jsonify({"code": 404, "msg": "Can't process request"}), 404)


@questions.route('/questions/<question_id>', methods=['GET'])
def get_question(question_id):
    if not question_id:
        return make_response(jsonify({"code": 412, "msg": "Precondition Failed"}, 412))
    question = None
    try:
        question = Question.query.filter_by(id=question_id).first()
        if question is None:
            return make_response(jsonify({"code": 404, "msg": "Doesn't exists"}), 404)

        db.session.close()
        return jsonify([row2dict(question)])
    except:
        print("Problem while getting an question")
        return make_response(jsonify({"code": 404, "msg": "Can't process request"}), 404)
    finally:
        db.session.close()

