"""
GOOGLE_APPLICATION_CREDENTIALS=<path to service account>
"""
from os import environ
from googleapiclient import discovery
from flask import jsonify, abort

SECRET_TOKEN = environ.get('TOKEN')


def auth_check(request):
    token = request.headers.get('X-Auth-Token')
    if not token or token != SECRET_TOKEN:
        abort(401)


def main(request):
    auth_check(request)
    service = discovery.build('compute', 'v1')
    project = environ.get("GCP_PROJECT")
    zones = environ.get("GCP_ZONES")
    request = service.disks().list(project=project, zone=zones)
    response = request.execute()
    print("TESTATAAN PRINTTAUSTA")
    return jsonify([item.get('name') for item in response.get('items')])
