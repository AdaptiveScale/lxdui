from flask import Blueprint, request
from flask import jsonify

from api.src.models.LXDModule import LXDModule
from api.src.models.LXCProfile import LXCProfile
from api.src.helpers.profile_schema import doValidate
from api.src.utils import response

profile_api = Blueprint('profile_api', __name__)


@profile_api.route('/')
def profiles():
    try:
        client = LXDModule()
        return response.reply(client.listProfiles())
    except ValueError as ex:
        return response.replyFailed(ex.__str__())


@profile_api.route('/', methods=['POST'])
def create_profile():
    data = request.get_json(silent=True)
    validate = doValidate(data)

    if validate:
        return response.replyFailed(message=validate.message, status=403)

    try:
        profile = LXCProfile(data)
        return jsonify(profile.createProfile())
    except ValueError as ex:
        return response.replyFailed(ex.__str__())


@profile_api.route('/<string:name>')
def get_profile(name):
    try:
        profile = LXCProfile({'name': name})
        return response.reply(profile.info())
    except ValueError as ex:
        return response.replyFailed(ex.__str__())


@profile_api.route('/<string:name>', methods=['DELETE'])
def delete_profile(name):
    try:
        profile = LXCProfile({'name': name})
        profile.deleteProfile()
        return response.reply()
    except ValueError as ex:
        return response.replyFailed(message=ex.__str__())


@profile_api.route('/', methods=['PUT'])
def update_profile():
    data = request.get_json()
    validation = doValidate(data)
    if validation:
        return response.replyFailed(message=validation.message)
    try:
        profile = LXCProfile(data)
        return response.reply(profile.updateProfile())
    except ValueError as ex:
        return response.replyFailed(message=ex.__str__())
