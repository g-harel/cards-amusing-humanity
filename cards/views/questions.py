from flask import Blueprint, jsonify, request, make_response
from domain.models.question import Question, row2dict
from datasource.database import db
from util.uuid_generator import UuidGenerator


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


@ ques.route('/questions', methods=['POST'])
def add_question():
    text = request.form.get('text')
    extension = request.form.get('extension')

    if not text or not extension:
        return make_response(jsonify({"code": 412, "msg": "Precondition Failed"}, 412))

    new_id = UuidGenerator().generate_uuid()
    new_question = Question(id=new_id, text=text, extension=extension)
    db.session.add(new_question)

    try:
        db.session.commit()
        return jsonify({"code": 200, "msg": "success"})
    except Exception as error:
        print("Problem while adding a question")
        print(error)
        db.session.rollback()
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    finally:
        db.session.close()


@ques.route('/questions/<question_id>', methods=['PUT'])
def update_question(question_id):
    text = request.form.get('text')
    extension = request.form.get('extension')
    
    if not text or not extension:
        return make_response(jsonify({"code": 412, "msg": "Precondition Failed"}, 412))
    
    db.session.query(Question).filter(Question.id == question_id)\
        .update({Question.text: text, Question.extension: extension})
    try:
        db.session.commit()
        return jsonify({"code": 200, "msg": "success"})
    except Exception as error:
        print("Problem while updating quesiont")
        print(error)
        db.session.rollback()
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    finally:
        db.session.close()
   
        
@ques.route('/questions/<question_id>', methods=['DELETE'])
def delete_question(question_id):
    if not question_id:
        return make_response(jsonify({"code": 412, "msg": "Precondition Failed"}, 412))
    
    try:
        question = Question.query.filter_by(id=question_id).first()
        current_db_session = db.session.object_session(question)
        current_db_session.delete(question)
        db.session.commit()
        return jsonify({"code": 200, "msg": "success"})
    except Exception as error:
        print("Problem while deleting question")
        print(error)
        db.session.rollback()
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    finally:
        db.session.close()

