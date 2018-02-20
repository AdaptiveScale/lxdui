from flask import Blueprint, request
from api.src.helpers.container_schema import doValidate

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
    client = LXCContainer({'name':name})
    return response.reply(client.info())


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

@container_api.route('/<string:name>', methods=['DELETE'])
def deleteContainer(name):
    input = request.get_json(silent=True)
    force = False if input == None else input.get('force')
    print(force)
    try:
        container = LXCContainer({'name': name})
        container.delete(force)
        return response.reply(None)
    except ValueError as ex:
        return response.reply(message=ex.__str__(), status=403)