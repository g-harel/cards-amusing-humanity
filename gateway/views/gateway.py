import redis
import os
import logging
from flask import Blueprint, request

gate = Blueprint('gate', __name__, url_prefix='/api')

# mem = redis.Redis(host="gateway-redis", port=6379, db=0)

# RATE_LIMIT  = int(float(os.getenv("RATE-LIMITING-THRESHOLD")))
# TIMEOUT = int(float(os.getenv("BLOCKED-IP-TIMEOUT")))

RATE_LIMIT = 3
TIMEOUT = 5
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
        print("Problem while getting IP")
        return True

    gunicorn_logger.info('IP Address: ' + str(IP))
    #TODO: Refresh DB, remove expired rate
    #TODO: Save the new IP entry or increment one
    #TODO Get new count and decide to block or allow
    return True


@gate.route('/game', methods=['GET'])
def get_game():
    """ Get Game with IP counting """
    deck = request.args.get('deck', default='Base', type=str)

    if(authorize_request(request)):
        return "authorized"
    else:
        return "unauthorized"


@gate.route('/submit', methods=['POST'])
def submit_game():
    """ Post a game with IP counting """
    if(authorize_request(request)):
        return "authorized"
    else:
        return "unauthorized"


