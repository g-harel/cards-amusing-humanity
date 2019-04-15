import os
import requests
import json
import ast
from flask import Blueprint, jsonify, make_response, request
from views.brewer import get_random_answer, get_random_question


game = Blueprint('game', __name__, url_prefix='')

@game.route('/game', methods=['GET'])
def get_new_game():
    """ Create and return a game object for user """

    deck = request.args.get('deck', default='Base', type=str)
    # Get env. number of answers
    num_answers_cards = os.getenv("DEFAULT_NUM_ANSWERS")

    # Get random cards
    answers = get_random_answer(num_answers_cards, deck)
    questions = get_random_question(1, deck)

    game_data = {
        "question": questions[0],
        "answers": answers
    }
    # # Sign the game
    res = requests.post("http://signing/sign", json={"payload" : game_data})

    if(res.status_code == 200):
        return_data = ast.literal_eval(res.text)
        return jsonify({'token':return_data['token']})

    return make_response(jsonify({"error": "Can't find resources"}), 404)