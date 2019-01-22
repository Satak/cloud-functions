from os import environ
from google.cloud import translate
from flask import jsonify, abort

SECRET_TOKEN = environ.get('TOKEN')


def auth_check(request):
    token = request.headers.get('X-Auth-Token')
    if not token or token != SECRET_TOKEN:
        abort(401)


def main(request):
    auth_check(request)
    translate_client = translate.Client()
    request_json = request.get_json(silent=True)
    text = request_json.get('text', '')
    if request.method == 'POST' and request_json and text:
        result = translate_client.detect_language(text)
        return jsonify(
            {
                'confidence': result['confidence'],
                'language': result['language']
            }
        )
    return jsonify({'data': 'Use post method and send JSON payload: {"text": "str"}'})
