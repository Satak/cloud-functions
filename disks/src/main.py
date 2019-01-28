"""
GOOGLE_APPLICATION_CREDENTIALS=<path to service account>
"""
from os import environ
from datetime import date
import logging
from googleapiclient import discovery
from flask import jsonify, abort

SECRET_TOKEN = environ.get('TOKEN')


def list_disks(disk_service, project, zone):
    request = disk_service.list(project=project, zone=zone)
    response = request.execute()
    return [item.get('name') for item in response.get('items')]


def take_snapshot(disk_service, disk_name, project, zone, body):
    request = disk_service.createSnapshot(project=project, zone=zone, disk=disk_name, body=body)
    response = request.execute()
    logging.info(f'Took snapshot on disk {disk_name}')
    return response


def get_project_zones(request):
    params = request.get_json(silent=True)
    if not params:
        logging.warn('Endpoint accessed without any payload')
        abort(400)
    project = params.get('project')
    zones = params.get('zones')
    if not all((project, zones)):
        logging.warn('Endpoint accessed without project or zones payload')
        abort(400)
    return project, zones


def auth_check(request):
    token = request.headers.get('X-Auth-Token')
    if not token or token != SECRET_TOKEN:
        logging.warn('Endpoint accessed with invalid credentials')
        abort(401)


def main(request):
    auth_check(request)
    if request.method == 'POST':
        project, zones = get_project_zones(request)
        date_str = date.today().isoformat()
        service = discovery.build('compute', 'v1')
        disk_service = service.disks()  # pylint: disable=E1101
        # snapshot_service = service.snapshots()  # pylint: disable=E1101
        disks = list_disks(disk_service, project, zones)
        for disk in disks:
            take_snapshot(disk_service, disk, project, zones, {'name': f'snapshot-test-{date_str}'})
        logging.info('Endpoint accessed with valid credentials')
        return jsonify(disks)
    else:
        return jsonify({'error': 'Method not allowed'}), 400
