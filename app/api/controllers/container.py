from flask import Blueprint, request
from flask_jwt import jwt_required
from app.api.schemas.container_schema import doValidate, doValidateCloneMove, doValidateImageExport

from app.api.models.LXCContainer import LXCContainer
from app.api.models.LXDModule import LXDModule
from app.api.utils import response

container_api = Blueprint('container_api', __name__)

@container_api.route('/')
@jwt_required()
def containers():
    client = LXDModule()
    return response.reply(client.listContainers())


@container_api.route('/<string:name>')
@jwt_required()
def getContainer(name):
    try:
        container = LXCContainer({'name': name})
        return response.replySuccess(container.info())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())



@container_api.route('/', methods=['POST'])
@jwt_required()
def createContainer():
    input = request.get_json(silent=True)
    validation = doValidate(input)
    if validation:
        return response.reply(message=validation.message, status=403)

    input = [input] if not isinstance(input, list) else input

    try:
        result = []
        for container in input:
            client = LXCContainer(container)
            result.append(client.create())
        return response.reply(result)
    except ValueError as ex:
        return response.reply(message=ex.__str__(), status=403)

@container_api.route('/', methods=['PUT'])
@jwt_required()
def updateContainer():
    input = request.get_json(silent=True)
    validation = doValidate(input)
    if validation:
        return response.reply(message=validation.message, status=403)

    try:
        client = LXCContainer(input)
        return response.reply(client.update())
    except ValueError as ex:
        return response.reply(message=ex.__str__(), status=403)


@container_api.route('/<string:name>', methods=['DELETE'])
@jwt_required()
def deleteContainer(name):
    input = request.get_json(silent=True)
    force = False if input == None else input.get('force')
    try:
        container = LXCContainer({'name': name})
        container.delete(force)
        return response.reply(None)
    except ValueError as ex:
        return response.replyFailed(message=ex.__str__())


@container_api.route('/start/<string:name>', methods=['PUT'])
@jwt_required()
def startContainer(name):
    try:
        container = LXCContainer({'name': name})
        container.start()
        return response.replySuccess(container.info())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@container_api.route('/stop/<string:name>', methods=['PUT'])
@jwt_required()
def stopContainer(name):
    try:
        container = LXCContainer({'name': name})
        container.stop()
        return response.replySuccess(container.info())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@container_api.route('/restart/<string:name>', methods=['PUT'])
@jwt_required()
def restartContainer(name):
    try:
        container = LXCContainer({'name': name})
        container.restart()
        return response.replySuccess(container.info())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())

@container_api.route('/clone/<string:name>', methods=['POST'])
@jwt_required()
def cloneContainer(name):
    input = request.get_json(silent=True)
    validation = doValidateCloneMove(input)
    if validation:
        return response.reply(message=validation.message, status=403)

    input['name'] = name
    try:
        container = LXCContainer(input)
        return response.replySuccess(container.clone())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())

@container_api.route('/move/<string:name>', methods=['POST'])
@jwt_required()
def moveContainer(name):
    input = request.get_json(silent=True)
    validation = doValidateCloneMove(input)
    if validation:
        return response.reply(message=validation.message, status=403)

    input['name'] = name
    try:
        container = LXCContainer(input)
        return response.replySuccess(container.move())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@container_api.route('/export/<string:name>', methods=['POST'])
@jwt_required()
def exportContainer(name):
    input = request.get_json(silent=True)
    validation = doValidateImageExport(input)
    if validation:
        return response.reply(message=validation.message, status=403)

    force = False if input.get('force') == None else input.get('force')
    input['name'] = name
    try:
        container = LXCContainer(input)
        return response.replySuccess(container.export(force))
    except ValueError as e:
        return response.replyFailed(message=e.__str__())