from flask import Blueprint, request, abort
from flask import jsonify

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
def get_container(name):
        client = LXCContainer({'name':name})
        return response.reply(client.info())

@container_api.route('/', methods=['POST'])
def create_container():
        input = request.get_json()
        validation = doValidate(input)
        if validation:
                return jsonify({'validationError':validation.message})
        try:
                client = LXCContainer(input)
                return jsonify(client.create())
        except ValueError as ex:
            return response.reply(ex.__str__(), 'Failed', 403)

@container_api.route('/<string:name>', methods=['DELETE'])
def deleteContainer(name):
    try:
        container = LXCContainer({'name': name})
        container.delete()
        return response.reply(None)
    except ValueError as ex:
        return response.reply(ex.__str__(), 'Failed', 403)