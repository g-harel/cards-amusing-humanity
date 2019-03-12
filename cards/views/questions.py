from flask import Blueprint, jsonify, make_response
from domain.models.question import Question, row2dict
from datasource.database import db


ques = Blueprint('questions', __name__, url_prefix='/api')


@ques.route('/questions', methods=['GET'])
def get_all_questions():
    questions_list = Question.query.all()
    db.session.close()
    return jsonify([row2dict(question) for question in questions_list])


@ques.route('/questions/<question_id>', methods=['GET'])
def get_question(question_id):
    if not question_id:
        return make_response(jsonify({"code": 412, "msg": "Precondition Failed"}, 412))
    question = None
    try:
        question = Question.query.filter_by(id=question_id).first()
        if question is None:
            return make_response(jsonify({"code": 404, "msg": "Doesn't exists"}), 404)
    except Exception as error:
        print("Problem while getting question")
        print(error)
        db.session.rollback()
    finally:
        db.session.close()
        return jsonify([row2dict(question)])
