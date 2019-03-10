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


@ans.route('/answers', methods=['POST'])
def add_answer():
    text = request.form.get('text')
    extension = request.form.get('extension')

    if not text or not extension:
        return make_response(jsonify({"code": 412, "msg": "Precondition Failed"}, 412))

    new_id = UuidGenerator().generate_uuid()
    new_answer = Answer(id=new_id, text=text, extension=extension)
    db.session.add(new_answer)
    try:
        db.session.commit()
        return jsonify({"code": 200, "msg": "success"})
    except Exception as error:
        print("Problem while saving answers")
        print(error)
        db.session.rollback()
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    finally:
        db.session.close()


@ans.route('/answers/<answer_id>', methods=['PUT'])
def update_answer(answer_id):
    text = request.form.get('text')
    extension = request.form.get('extension')

    if not text or not extension or not answer_id:
        return make_response(jsonify({"code": 412, "msg": "Precondition Failed"}, 412))

    db.session.query(Answer).filter(Answer.id == answer_id).\
        update({Answer.text: text, Answer.extension: extension})

    try:
        db.session.commit()
        return jsonify({"code": 200, "msg": "success"})
    except Exception as error:
        print("Problem while updating")
        print(error)
        db.session.rollback()
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    finally:
        db.session.close()


@ans.route('/answers/<answer_id>', methods=['DELETE'])
def delete_answers(answer_id):
    if not answer_id:
        return make_response(jsonify({"code": 412, "msg": "Precondition Failed"}, 412))

    try:
        answer = Answer.query.filter_by(id=answer_id).first()
        current_db_session = db.session.object_session(answer)
        current_db_session.delete(answer)
        db.session.commit()
        return jsonify({"code": 200, "msg": "success"})
    except Exception as error:
        print("Problem while deleting")
        print(error)
        db.session.rollback()
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    finally:
        db.session.close()
