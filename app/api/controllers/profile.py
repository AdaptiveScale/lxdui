from flask import Blueprint, request
from flask import jsonify
from flask_jwt_extended import jwt_required

from app.api.models.LXDModule import LXDModule
from app.api.models.LXCProfile import LXCProfile
from app.api.schemas.profile_schema import doValidate, doValidateRename
from app.api.utils import response

profile_api = Blueprint('profile_api', __name__)


@profile_api.route('/')
@jwt_required()
def profiles():
    try:
        client = LXDModule()
        return response.reply(client.listProfiles())
    except ValueError as ex:
        return response.replyFailed(ex.__str__())


@profile_api.route('/', methods=['POST'])
@jwt_required()
def create_profile():
    input = request.get_json(silent=True)
    validation = doValidate(input)
    if validation:
        return response.replyFailed(message=validation.message)

    try:
        profile = LXCProfile(input)
        return response.replySuccess(profile.createProfile(), message='Profile {} created successfully.'.format(input.get('name')))
    except ValueError as ex:
        return response.replyFailed(ex.__str__())


@profile_api.route('/<string:name>')
@jwt_required()
def get_profile(name):
    try:
        profile = LXCProfile({'name': name})
        return response.reply(profile.info(name))
    except ValueError as ex:
        return response.replyFailed(ex.__str__())


@profile_api.route('/<string:name>', methods=['DELETE'])
@jwt_required()
def delete_profile(name):
    try:
        profile = LXCProfile({'name': name})
        profile.deleteProfile()
        return response.replySuccess(data=None, message='Profile {} deleted successfully.'.format(name))
    except ValueError as ex:
        return response.replyFailed(message=ex.__str__())


@profile_api.route('/<string:name>', methods=['PUT'])
@jwt_required()
def update_profile(name):
    data = request.get_json()
    data['name'] = name
    validation = doValidate(data)
    if validation:
        return response.replyFailed(message=validation.message)
    try:
        profile = LXCProfile(data)
        return response.replySuccess(profile.updateProfile(), message='Profile {} updated successfully.'.format(name))
    except ValueError as ex:
        return response.replyFailed(message=ex.__str__())


@profile_api.route('/rename/<string:name>', methods=['PUT'])
@jwt_required()
def rename(name):
    data = request.get_json()
    validation = doValidateRename(data)

    if validation:
        return response.replyFailed(message=validation.message)

    try:
        data['name'] = name
        profile = LXCProfile(data)
        return response.reply(profile.rename())
    except ValueError as ex:
        return response.replyFailed(message=ex.__str__())
