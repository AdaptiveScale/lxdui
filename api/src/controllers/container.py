from flask import Blueprint, request
from api.src.helpers.container_schema import doValidate, doValidateCloneMove

from api.src.models.LXCContainer import LXCContainer
from api.src.models.LXDModule import LXDModule
from api.src.utils import response

container_api = Blueprint('container_api', __name__)

@container_api.route('/')
def containers():
    client = LXDModule()
    return response.reply(client.listContainers())


@container_api.route('/<string:name>')
def getContainer(name):
    try:
        container = LXCContainer({'name': name})
        return response.replySuccess(container.info())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())



@container_api.route('/', methods=['POST'])
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
def startContainer(name):
    try:
        container = LXCContainer({'name': name})
        container.start()
        return response.replySuccess(container.info())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@container_api.route('/stop/<string:name>', methods=['PUT'])
def stopContainer(name):
    try:
        container = LXCContainer({'name': name})
        container.stop()
        return response.replySuccess(container.info())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@container_api.route('/restart/<string:name>', methods=['PUT'])
def restartContainer(name):
    try:
        container = LXCContainer({'name': name})
        container.restart()
        return response.replySuccess(container.info())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())

@container_api.route('/clone/<string:name>', methods=['POST'])
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