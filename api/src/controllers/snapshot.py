from flask import Blueprint, request

from api.src.models.LXCSnapshot import LXCSnapshot
from api.src.utils import response

snapshot_api = Blueprint('snapshot_api', __name__)

@snapshot_api.route('/container/<string:container>')
def containerSnapshots(container):
    try:
        snapshot = LXCSnapshot({'container': container})
        return response.replySuccess(snapshot.snapshotList())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@snapshot_api.route('/<string:name>/container/<string:container>')
def snapshotInfo(name, container):
    print(name)
    try:
        snapshot = LXCSnapshot({'container': container, 'name': name})
        return response.replySuccess(snapshot.snapshotInfo())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())



@snapshot_api.route('/<string:name>/container/<string:container>', methods=['POST'])
def createSnapshot(name, container):
    try:
        snapshot = LXCSnapshot({'name': name, 'container': container})
        return response.replySuccess(snapshot.snapshot())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@snapshot_api.route('/<string:name>/container/<string:container>', methods=['DELETE'])
def deleteSnapshot(name, container):
    try:
        snapshot = LXCSnapshot({'name': name, 'container': container})
        return response.replySuccess(snapshot.snapshotDelete())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())