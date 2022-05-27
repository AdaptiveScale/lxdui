from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.api.schemas.container_schema import doValidate, doValidateCloneMove, doValidateImageExport

from app.api.models.LXCContainer import LXCContainer
from app.api.models.LXDModule import LXDModule
from app.api.utils import response
from app.api.utils.containerMapper import getContainerDetails

container_api = Blueprint('container_api', __name__)

@container_api.route('/')
@jwt_required()
def containers():
    client = LXDModule()
    result = []
    containers = client.listContainers()
    result = []
    for container in containers:
        result.append(getContainerDetails(container))

    return response.reply(result)


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
    validation = doValidate(input, LXDModule().setLimitsCPU())
    if validation:
        return response.reply(message=validation.message, status=403)

    input = [input] if not isinstance(input, list) else input

    try:
        result = []
        for container in input:
            client = LXCContainer(container)
            result.append(client.create())
        return response.reply(result, message='Container {} created successfully.'.format(container.get('name')))
    except ValueError as ex:
        return response.reply(message=ex.__str__(), status=403)

@container_api.route('/', methods=['PUT'])
@jwt_required()
def updateContainer():
    input = request.get_json(silent=True)
    validation = doValidate(input, LXDModule().setLimitsCPU())
    if validation:
        return response.reply(message=validation.message, status=403)

    try:
        client = LXCContainer(input)
        return response.reply(client.update(), message='Container {} updated successfully.'.format(input.get('name')))
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
        return response.reply(None, message='Container {} deleted successfully.'.format(name))
    except ValueError as ex:
        return response.replyFailed(message=ex.__str__())


@container_api.route('/start/<string:name>', methods=['PUT'])
@jwt_required()
def startContainer(name):
    try:
        container = LXCContainer({'name': name})
        container.start()
        return response.replySuccess(container.info(), message='Container {} started successfully.'.format(name))
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@container_api.route('/stop/<string:name>', methods=['PUT'])
@jwt_required()
def stopContainer(name):
    try:
        container = LXCContainer({'name': name})
        ephemeral = container.info()['ephemeral']
        container.stop()
        if ephemeral:
            return response.replySuccess(container.info(), message='Container {} stopped successfully.'.format(name))
        return response.replySuccess(container.info(), message='Container {} stopped successfully.'.format(name))
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@container_api.route('/restart/<string:name>', methods=['PUT'])
@jwt_required()
def restartContainer(name):
    try:
        container = LXCContainer({'name': name})
        container.restart()
        return response.replySuccess(container.info(), message='Container {} restarted successfully.'.format(name))
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
        return response.replySuccess(container.clone(), message='Container {} cloned successfully.'.format(name))
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
        return response.replySuccess(container.move(), message='Container {} moved successfully.'.format(name))
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
        return response.replySuccess(container.export(force), message='Image {} exported successfully from container {}.'.format(input.get('imageAlias'), name))
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@container_api.route('/freeze/<string:name>', methods=['PUT'])
@jwt_required()
def freezeContainer(name):
    try:
        container = LXCContainer({'name': name})
        container.freeze()
        return response.replySuccess(container.info(), message='Container {} is frozen.'.format(name))
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@container_api.route('/unfreeze/<string:name>', methods=['PUT'])
@jwt_required()
def unfreezeContainer(name):
    try:
        container = LXCContainer({'name': name})
        container.unfreeze()
        return response.replySuccess(container.info(), message='Container {} is unfrozen.'.format(name))
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@container_api.route('/network/<name>/add', methods=['POST'])
@jwt_required()
def addNetwork(name):
    input = request.get_json(silent=True)
    try:
        container = LXCContainer({'name': name})
        return response.replySuccess(container.addNetwork(input))
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@container_api.route('/network/<name>/remove/<network>', methods=['DELETE'])
@jwt_required()
def removeNetwork(name, network):
    try:
        container = LXCContainer({'name': name})
        return response.replySuccess(container.removeNetwork(network))
    except ValueError as e:
        return response.replyFailed(message=e.__str__())

@container_api.route('/proxy/<name>/add/<proxy>', methods=['POST'])
@jwt_required()
def addProxy(name, proxy):
    input = request.get_json(silent=True)
    try:
        container = LXCContainer({'name': name})
        return response.replySuccess(container.addProxy(proxy, input))
    except ValueError as e:
        return response.replyFailed(message=e.__str__())

@container_api.route('/proxy/<name>/remove/<proxy>', methods=['DELETE'])
@jwt_required()
def removeProxy(name, proxy):
    try:
        container = LXCContainer({'name': name})
        return response.replySuccess(container.removeProxy(proxy))
    except ValueError as e:
        return response.replyFailed(message=e.__str__())
