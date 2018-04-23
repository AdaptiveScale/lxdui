from flask import Blueprint, request
from flask_jwt import jwt_required
from app.api.schemas.container_schema import doValidateCloneMove

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


@snapshot_api.route('/<string:name>/container/<string:container>', methods=['PUT'])
@jwt_required()
def restoreSnapshot(name, container):
    try:
        snapshot = LXCSnapshot({'name': name, 'container': container})
        return response.replySuccess(snapshot.snapshotRestore())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@snapshot_api.route('/<string:name>/container/<string:container>/publish', methods=['POST'])
@jwt_required()
def publishSnapshot(name, container):
    try:
        snapshot = LXCSnapshot({'name': name, 'container': container})
        return response.replySuccess(snapshot.snapshotPublish())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())

@snapshot_api.route('/<string:name>/container/<string:container>/create', methods=['POST'])
@jwt_required()
def createContainerSnapshot(name, container):
    input = request.get_json(silent=True)
    validation = doValidateCloneMove(input)
    if validation:
        return response.reply(message=validation.message, status=403)

    input['name'] = name
    input['container'] = container
    try:
        snapshot = LXCSnapshot(input)
        return response.replySuccess(snapshot.snapshotCreateContainer())
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


