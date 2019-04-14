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

    extension = request.args.get('extension', default='Base', type=str)
    # Get env. number of answers
    num_answers_cards = os.getenv("DEFAULT_NUM_ANSWERS")
    
    # Get random cards
    answers = get_random_answer(num_answers_cards, extension)
    questions = get_random_question(1, extension)
    
    game_data = {
        "question": questions,
        "answers": answers
    }
    
    # Convert dictionary to json and then to string
    json_game = str(game_data)
    # # Sign the game
    res = requests.post("http://signing/sign", json={"payload" : {"game": json_game}})

    if(res.status_code == 200):
        return_data = ast.literal_eval(res.text)
        return make_response(jsonify({'token':return_data['token']}, 200))
    
    return make_response(jsonify({"error": "Can't find resources"}), 404)