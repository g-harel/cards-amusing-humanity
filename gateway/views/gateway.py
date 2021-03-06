import os
import logging
import time
import ast
import requests
from flask import Blueprint, jsonify, request, make_response


gate = Blueprint('gate', __name__, url_prefix='/api')

# Rate Limiting
RATE_LIMIT  = int(os.getenv("RATE_LIMITING_THRESHOLD"))
TIMEOUT = int(os.getenv("BLOCKED_IP_TIMEOUT"))
# Logger from Gunicorn allowing to see log message in kube.
gunicorn_logger = logging.getLogger('gunicorn.error')


# TODO: (extra) make a second request counter for static file 
def authorize_request(Request, memdb):
    """ Authorize a request  """
    ip = None
    try:
        forwarded_ip = Request.environ.get('HTTP_X_FORWARDED_FOR')
        if forwarded_ip is None:
            ip = Request.environ.get('REMOTE_ADDR')
        else:
            ip = request.environ.get('HTTP_X_FORWARDED_FOR')
    except:
        gunicorn_logger.info("Can not get IP Address")
        return True

    gunicorn_logger.info('IP Address: ' + str(ip))

    ip_data = None
    ip = str(ip)
    try:
        ip_data = memdb.get(memdb, key=ip)
    except Exception as error:
        gunicorn_logger.info(error)

    if ip_data[1] is None:
        # Case where it's a new IP
        date_n = int(time.time())
        default_data = {
            'ip': ip,
            'counter': 0,
            'last_transaction': date_n
        }
        memdb.set(memdb, key=ip, data=default_data)
        return True


    # Case where it's same IP again
    previous_count = int(ip_data[1])
    new_count = 0
    if previous_count > RATE_LIMIT:
        # Case where the user used the service too much
        threshold_datetime = int(ip_data[2])
        threshold_datetime = threshold_datetime + (60*TIMEOUT)
        if int(time.time()) > threshold_datetime:
            # Reset Counter and allow user again
            gunicorn_logger.info("Reset Counter")
            new_count = 0
        else:
            # Block transaction 
            gunicorn_logger.info("Blocking transaction")
            return False
    else:
        new_count = int(previous_count) + 1
    
    gunicorn_logger.info("Increment Counter")
    date_now = int(time.time())
    new_data = {
        'ip': ip,
        'counter': new_count,
        'last_transaction': date_now
    }
    memdb.set(memdb, key=ip, data=new_data)
    return True


@gate.route('/game', methods=['GET'])
def get_game():
    """ Get Game with IP counting """
    from memory.rstorage import RedisStorage
    deck = request.args.get('deck', default='mini', type=str)
    if authorize_request(request, RedisStorage):
        url = "http://cards/game?deck="+deck
        resp = requests.get(url)
        if resp.status_code == 200:
            dict_respn = ast.literal_eval(resp.text)
            return make_response(jsonify({"token": dict_respn['token']}), 200)
    
    return make_response(jsonify({"error": "Not Found"}), 404)


@gate.route('/submit', methods=['POST'])
def submit_game():
    """ Post a game with IP counting """
    from memory.rstorage import RedisStorage
    if authorize_request(request, RedisStorage):
        resp = requests.post("http://analytics/submit", json=request.get_json())
        if resp.status_code == 200:
            dict_resp =  ast.literal_eval(resp.text)
            return make_response(jsonify({"similarity": dict_resp['similarity']}), 200)

    return make_response(jsonify({"error": "Not Found"}), 404)
