import redis
import os
import logging
import time
import ast
import requests
from flask import Blueprint, jsonify, request, make_response

gate = Blueprint('gate', __name__, url_prefix='/api')

memdb = redis.Redis(host="gateway-redis", port=6379, db=0)

RATE_LIMIT  = int(os.getenv("RATE_LIMITING_THRESHOLD"))
TIMEOUT = int(os.getenv("BLOCKED_IP_TIMEOUT"))

gunicorn_logger = logging.getLogger('gunicorn.error')

# Grabing the IP from user's request
def authorize_request(Request):
    IP = None
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

    IP_data = None
    IP = str(IP)
    try:
        gunicorn_logger.info('get data')
        IP_data = memdb.hmget(IP, ['ip', 'counter', 'last_transaction'])

    except Exception as error:
        gunicorn_logger.info(error)
    
    
    if IP_data[0] is None:
        # Case where it's a new IP
        date_n = int(time.time())
        memdb.hmset(IP, {'ip': IP, 'counter': 0, 'last_transaction': date_n})
        return True


    gunicorn_logger.info("Known Client !!!")

    # Case where it's same IP again
    previous_count = int(IP_data[1])
    new_count = 0
    if previous_count > RATE_LIMIT:
        # Case where the user used the service too mutch
        threshold_datetime = int(IP_data[2])
        threshold_datetime = threshold_datetime +  (60*TIMEOUT)
        if int(time.time()) > threshold_datetime:
            # Reset Coutner and allow user again
            gunicorn_logger.info("Reset Counter")
            new_count = 0
        else:
            # Block transaction 
            gunicorn_logger.info("Blocking transaction")
            return False
    else:
        new_count = int(previous_count)  + 1
    
    gunicorn_logger.info("Increment Counter")
    date_now = int(time.time())
    memdb.hmset(IP, {'ip': IP, 'counter': new_count, 'last_transaction': date_now})
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


