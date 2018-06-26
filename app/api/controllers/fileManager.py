from flask import Blueprint, request
from flask import jsonify
from flask_jwt import jwt_required

from app.api.models.LXCFileManager import LXCFileManager
from app.api.utils import response

import json

file_manager_api = Blueprint('file_manager_api', __name__)


@file_manager_api.route('/container/<string:name>')
@jwt_required()
def list(name):
    path = request.args.get('path')
    if path == None:
        return jsonify([])
        #return response.replyFailed('Path is missing')

    input = {}
    input['name'] = name
    input['path'] = path

    try:
        fileManager = LXCFileManager(input)
        try:
            results = []
            #Folder
            items = json.loads(fileManager.download().decode('utf-8'))['metadata']
            for item in items:
                input['path'] = path + '/' + item
                results.append({
                    'title': item,
                    'key': item,
                    'folder': isFolder(LXCFileManager(input)),
                    'lazy': isFolder(LXCFileManager(input)),
                })

            return jsonify(results)
            return response.reply(results)
        except:
            #File
            return jsonify([])
            return response.replyFailed('Please enter a valid directory path')
            #result = fileManager.download()

    except ValueError as ex:
        return response.replyFailed(ex.__str__())


def isFolder(fileManager):
    try:
        # Folder
        result = json.loads(fileManager.download().decode('utf-8'))['metadata']
        return True
    except:
        # File
        result = fileManager.download()
        return False


#List directory or open file
@file_manager_api.route('/container/<string:name>', methods=['PUT'])
@jwt_required()
def download(name):
    input = request.get_json(silent=True)
    input['name'] = name

    try:
        fileManager = LXCFileManager(input)

        try:
            # Folder
            result = json.loads(fileManager.download().decode('utf-8'))['metadata']
        except:
            # File
            result = fileManager.download()

        return response.reply(result)
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
