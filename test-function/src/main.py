from os import environ
import logging
from flask import jsonify, abort

SECRET_TOKEN = environ.get('TOKEN')


def auth_check(request):
    token = request.headers.get('X-Auth-Token')
    if not token or token != SECRET_TOKEN:
        logging.warn('Endpoint accessed with invalid credentials')
        abort(401)


def main(request):
    auth_check(request)
    if request.method == 'POST':
        try:
            payload = request.get_json(silent=True)
            data = {
                'project': payload.get('project'),
                'zones': payload.get('zones')
            }
            logging.info(f'Endpoint accessed with valid credentials and payload: {data}')
            return jsonify(data)
        except Exception as err:
            logging.error(f'Endpoint crashed: {err}')
            return jsonify({'error': f'Payload error: {err}'})
    logging.warn('Endpoint accessed with invalid method')
    return jsonify({'error': 'Method not supported'})
