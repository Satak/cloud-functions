"""
GOOGLE_APPLICATION_CREDENTIALS=<path to service account>
"""
from os import environ
import json
from datetime import date
import logging
from googleapiclient import discovery
from flask import jsonify, abort

SECRET_TOKEN = environ.get('TOKEN')


def list_disks(disk_service, project, zone):
    request = disk_service.list(project=project, zone=zone)
    result = request.execute()
    return result['items']


def take_snapshot(disk_service, disk, project, zone):
    if not disk.get('description') or '-pool-' in disk.get('name', ''):
        logging.info(f'No description found from disk. Skipped disk {disk.get("name")}')
        return None
    date_str = date.today().isoformat()
    description = None
    try:
        description = json.loads(disk.get('description'))
        pvc = description.get('kubernetes.io/created-for/pvc/name', '')
        namespace = description.get('kubernetes.io/created-for/pvc/namespace', '')
        body = {
            'name': f'{pvc}-{namespace}-{date_str}',
            'description': disk.get('description')
        }
        request = disk_service.createSnapshot(project=project, zone=zone, disk=disk['name'], body=body)
        response = request.execute()
        logging.info(f'Snapshot OK. PVC: {pvc} Namespace: {namespace} Zone: {zone}')
        return response
    except Exception as err:
        logging.error(f'Error while taking a snapshot: {err}')


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
    return project, [zone.strip() for zone in zones.split(',')]


def auth_check(request):
    token = request.headers.get('X-Auth-Token')
    if not token or token != SECRET_TOKEN:
        logging.warn('Endpoint accessed with invalid credentials')
        abort(401)


def main(request):
    auth_check(request)
    if request.method == 'POST':
        project, zones = get_project_zones(request)
        service = discovery.build('compute', 'v1')
        disk_service = service.disks()  # pylint: disable=E1101
        # snapshot_service = service.snapshots()  # pylint: disable=E1101
        for zone in zones:
            disks = list_disks(disk_service, project, zone)
            for disk in disks:
                take_snapshot(disk_service, disk, project, zone)

        logging.info('Endpoint accessed with valid credentials')
        return jsonify({'data': 'Snapshots done'})
    else:
        return jsonify({'error': 'Method not allowed'}), 400
