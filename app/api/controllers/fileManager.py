from flask import Blueprint, request
from flask import jsonify
from flask_jwt import jwt_required

from app.api.models.LXCFileManager import LXCFileManager
from app.api.utils import response

file_manager_api = Blueprint('file_manager_api', __name__)


@file_manager_api.route('/container/<string:name>')
@jwt_required()
def list():
    try:
        fileManager = LXCFileManager()
        return response.reply(fileManager.list())
    except ValueError as ex:
        return response.replyFailed(ex.__str__())


@file_manager_api.route('/container/<string:name>', methods=['PUT'])
@jwt_required()
def download(name):
    input = request.get_json(silent=True)
    input['name'] = name

    try:
        fileManager = LXCFileManager(input)
        return response.reply(fileManager.download())
    except ValueError as ex:
        return response.replyFailed(ex.__str__())


@file_manager_api.route('/container/<string:name>', methods=['POST'])
@jwt_required()
def upload_file(name):
    input = request.get_json(silent=True)
    #validation = doValidate(input)
    # if validation:
    #     return response.replyFailed(message=validation.message)

    input['name'] = name

    try:
        fileManager = LXCFileManager(input)
        return response.reply(fileManager.push())
    except ValueError as ex:
        return response.replyFailed(ex.__str__())


@file_manager_api.route('/container/<string:name>', methods=['DELETE'])
@jwt_required()
def delete_profile(name):
    input = request.get_json(silent=True)
    # validation = doValidate(input)
    # if validation:
    #     return response.replyFailed(message=validation.message)

    input['name'] = name

    try:
        fileManager = LXCFileManager(input)
        fileManager.delete()
        return response.reply()
    except ValueError as ex:
        return response.replyFailed(message=ex.__str__())
