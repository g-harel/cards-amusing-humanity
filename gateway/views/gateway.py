import redis
import os
import logging
import datetime
import ast
import requests
from flask import Blueprint, jsonify, request, make_response

gate = Blueprint('gate', __name__, url_prefix='/api')

# memdb = redis.Redis(host="127.0.0.1", port=6379, db=0)

# RATE_LIMIT  = int(float(os.getenv("RATE-LIMITING-THRESHOLD")))
# TIMEOUT = int(float(os.getenv("BLOCKED-IP-TIMEOUT")))

RATE_LIMIT = 3
TIMEOUT = 5
gunicorn_logger = logging.getLogger('gunicorn.error')

# Grabing the IP from user's request
def authorize_request(Request):
    IP = None
    return True
    try:
        forwarded_ip = Request.environ.get('HTTP_X_FORWARDED_FOR')
        if forwarded_ip is None:
            IP = Request.environ.get('REMOTE_ADDR')
        else:
            IP = request.environ.get('HTTP_X_FORWARDED_FOR')
    except:
        gunicorn_logger.info("Can not get IP Address")
        return True

    gunicorn_logger.info('IP Address: ' + str(IP))
    try:
        IP_data = memdb.hmget(IP)
    except:
        gunicorn_logger("New IP client")
    
    
    if IP_data is None:
        # Case where it's a new IP
        data = {
            'IP': IP,
            'Counter' : 0,
            'Date': datetime.datetime.now()
        }
        memdb.hmset(IP, data)
        return True
    
    # Case where it's same IP again
    gunicorn_logger.info('from db ' + str(IP_data))

    #TODO: Refresh DB, remove expired rate
    #TODO: Save the new IP entry or increment one
    #TODO Get new count and decide to block or allow
    return True


@gate.route('/game', methods=['GET'])
def get_game():
    """ Get Game with IP counting """
    deck = request.args.get('deck', default='mini', type=str)
    if(authorize_request(request)):
        url = "http://cards/game?deck="+deck
        resp = requests.get(url)
        if resp.status_code == 200:
            dict_respn = ast.literal_eval(resp.text)
            return make_response(jsonify({"token": dict_respn['token']}))
    
    return make_response(jsonify({"error": "Not Found"}, 404))


@gate.route('/submit', methods=['POST'])
def submit_game():
    """ Post a game with IP counting """
    if(authorize_request(request)):
        resp = requests.post("http://analytics/submit", json=request.get_json())
        if resp.status_code == 200:
            dict_resp =  ast.literal_eval(resp.text)
            return make_response(jsonify({"similarity": dict_resp['similarity']}))
         

    return make_response(jsonify({"error": "Not Found"}, 404))


