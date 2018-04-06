from flask import Blueprint, request
from flask_jwt import jwt_required

from app.api.models.LXCSnapshot import LXCSnapshot
from app.api.utils import response

snapshot_api = Blueprint('snapshot_api', __name__)

@snapshot_api.route('/container/<string:container>')
@jwt_required()
def containerSnapshots(container):
    try:
        snapshot = LXCSnapshot({'container': container})
        return response.replySuccess(snapshot.snapshotList())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@snapshot_api.route('/<string:name>/container/<string:container>')
@jwt_required()
def snapshotInfo(name, container):
    print(name)
    try:
        snapshot = LXCSnapshot({'container': container, 'name': name})
        return response.replySuccess(snapshot.snapshotInfo())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())



@snapshot_api.route('/<string:name>/container/<string:container>', methods=['POST'])
@jwt_required()
def createSnapshot(name, container):
    try:
        snapshot = LXCSnapshot({'name': name, 'container': container})
        return response.replySuccess(snapshot.snapshot())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@snapshot_api.route('/<string:name>/container/<string:container>', methods=['DELETE'])
@jwt_required()
def deleteSnapshot(name, container):
    try:
        snapshot = LXCSnapshot({'name': name, 'container': container})
        return response.replySuccess(snapshot.snapshotDelete())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())