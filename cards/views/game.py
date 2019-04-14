import os
from flask import Blueprint, jsonify, make_response, request
from views.brewer import get_random_answer, get_random_question
from models.answers import row2dict
from models.questions import row2dict


game = Blueprint('game', __name__, url_prefix='')

@game.route('/game', methods=['GET'])
def get_new_game():
    """ Create and return a game object for user """
    deck = request.args.get('deck', default='Base', type=str)
    token = request.args.get('token', default='', type=str)

    # Verify Token 
    #//TODO: Verify Token
    num_answers_cards = 5
    # TODO: Replace by os.getenv("DEFAULT_NUM_ANSWERS")
    answers = get_random_answer(num_answers_cards, deck)
    questions = get_random_question(1, deck)
    game_data = {
        "token": token,
        "question": questions[0],
        "answers": answers
    }

    return make_response(jsonify({"game":game_data}), 200)