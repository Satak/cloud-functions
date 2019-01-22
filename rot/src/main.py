from os import environ
from string import ascii_lowercase as lc, ascii_uppercase as uc
from flask import jsonify, abort

SECRET_TOKEN = environ.get('TOKEN')


def auth_check(request):
    token = request.headers.get('X-Auth-Token')
    if not token or token != SECRET_TOKEN:
        abort(401)


def rot_encode(text, rot):
    trans = str.maketrans(lc + uc, lc[rot:] + lc[:rot] + uc[rot:] + uc[:rot])
    return str.translate(text, trans)


def main(request):
    auth_check(request)
    if request.method == 'POST':
        request_json = request.get_json(silent=True)
        message = request_json.get('message')
        rot = request_json.get('rot')
        if message and rot and isinstance(message, str) and isinstance(rot, int):
            output = rot_encode(message, rot)
            return jsonify({'data': output})
        else:
            return jsonify({'error': 'You must send JSON payload: {"message": "str", "rot": int}'}), 400
    return jsonify({'data': 'Use post method and send JSON payload: {"message": "str", "rot": int}'})
