from flask import Blueprint, jsonify, make_response
from database import db
import random
from models.answers import Answer, row2dict
from models.questions import Question, row2dict

game = Blueprint('game', __name__, url_prefix='')

@game.route('/game', methods=['GET'])
def get_new_game(number_of_item):
    """Obtain X number of random answers from database"""
    random_answers = []
    try:
        number_of_item_int = int(number_of_item)
        if type(number_of_item_int) is not int:
            return make_response(jsonify({"code": 412, "msg": "type has to be integer"}), 404)
        if number_of_item_int > MAXIMUM_CARD:
            return make_response(jsonify({"code": 412, "msg": "number is too large"}), 412)
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
    except ValueError:
        return make_response(jsonify({"code": 404, "msg": "Not Found"}), 404)
    except Exception as error:
        print("Problem while getting random answers")
        print(error)
        return make_response(jsonify({"code": 404, "msg": error}), 404)

    finally:
        db.session.close()