from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.api.models.LXDModule import LXDModule
from app.api.models.LXCStoragePool import LXCStoragePool
from app.api.schemas.storagePoolSchema import doValidate
from app.api.utils import response

storage_pool_api = Blueprint('storage_pool_api', __name__)


@storage_pool_api.route('/')
@jwt_required()
def storagePools():
    try:
        client = LXDModule()
        return response.reply(client.listStoragePools())
    except ValueError as ex:
        return response.replyFailed(ex.__str__())


@storage_pool_api.route('/', methods=['POST'])
@jwt_required()
def create_storage_pool():
    input = request.get_json(silent=True)
    validation = doValidate(input)
    if validation:
        return response.replyFailed(message=validation.message)

    try:
        storagePool = LXCStoragePool(input)
        return response.replySuccess(storagePool.createStoragePool(), message='Storage Pool {} created successfully.'.format(input.get('name')))
    except ValueError as ex:
        return response.replyFailed(ex.__str__())


@storage_pool_api.route('/<string:name>')
@jwt_required()
def get_storage_pool(name):
    try:
        storagePool = LXCStoragePool({'name': name})
        return response.reply(storagePool.info(name))
    except ValueError as ex:
        return response.replyFailed(ex.__str__())


@storage_pool_api.route('/<string:name>', methods=['DELETE'])
@jwt_required()
def delete_storage_pool(name):
    try:
        storagePool = LXCStoragePool({'name': name})
        storagePool.deleteStoragePool()
        return response.replySuccess(data=None, message='Storage Pool {} deleted successfully.'.format(name))
    except ValueError as ex:
        return response.replyFailed(message=ex.__str__())


@storage_pool_api.route('/<string:name>', methods=['PUT'])
@jwt_required()
def update_storage_pool(name):
    data = request.get_json()
    data['name'] = name
    validation = doValidate(data)
    if validation:
        return response.replyFailed(message=validation.message)
    try:
        storagePool = LXCStoragePool(data)
        return response.replySuccess(storagePool.updateProfile(), message='Storage Pool {} updated successfully.'.format(name))
    except ValueError as ex:
        return response.replyFailed(message=ex.__str__())
