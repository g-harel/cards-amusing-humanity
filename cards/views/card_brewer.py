from flask import Blueprint, jsonify, make_response
from datasource.database import db
import random
import datetime
from domain.models.answer import Answer, row2dict
from domain.models.history import History
from domain.models.question import Question, row2dict
from util.uuid_generator import UuidGenerator

brew = Blueprint('brewer', __name__, url_prefix='/api/brewer')


@brew.route('/answers/<number_of_item>', methods=['GET'])
def get_random_answer(number_of_item):
    """Obtain X number of random answers from database"""
    random_answers = []
    number_of_item_int = int(number_of_item)
    if type(number_of_item_int) is not int:
        return make_response(jsonify({"code": 404, "msg": "type has to be integer"}), 404)
    try:
        counter = 0
        while counter < number_of_item_int:
            random_index = random.randrange(0, db.session.query(Answer).count())
            row = db.session.query(Answer)[random_index]
            # Making sure data are unique
            if not random_answers.__contains__(row):
                random_answers.append(row)
                counter = counter + 1

        db.session.close()
        return jsonify([row2dict(answer) for answer in random_answers])
    except Exception as error:
        print("Problem while getting random answers")
        print(error)
        return make_response(jsonify({"code": 404, "msg": error}), 404)


@brew.route('/questions/<number_of_item>', methods=['GET'])
def get_random_question(number_of_item):
    """Obtain X number of questions from database"""
    random_questions = []
    number_of_item_int = int(number_of_item)
    if type(number_of_item_int) is not int:
        return make_response(jsonify({"code": 404, "msg": "type has to be integer"}), 404)

    try:
        counter = 0
        while counter < number_of_item_int:
            random_index = random.randrange(0, db.session.query(Question).count())
            row = db.session.query(Question)[random_index]
            # Making sure data are unique
            if not random_questions.__contains__(row):
                random_questions.append(row)
                counter = counter + 1

        for question in random_questions:
            new_id = UuidGenerator().generate_uuid()
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_his = History(id=new_id, card_id=question.id,
                              text_sent=question.text,
                              time_sent=now)
            db.session.add(new_his)

        db.session.commit()
        return jsonify([row2dict(question) for question in random_questions])
    except Exception as error:
        print("Problem while getting random questions")
        print(error)
        db.session.rollback()
        return make_response(jsonify({"code": 404, "msg": error}), 404)

    finally:
        db.session.close()
