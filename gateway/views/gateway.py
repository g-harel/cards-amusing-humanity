import redis
from flask import Blueprint, request

gate = Blueprint('gate', __name__, url_prefix='/api')

# mem = redis.Redis(host="gateway-redis", port=6379, db=0)


# Grabing the IP from user's request
def authorize_request(Request):
    print(Request.headers)
    print("IP")
    print(Request.remote_addr)
    print("IP 2")
    print(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
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


