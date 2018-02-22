from flask import Blueprint, request
from flask import jsonify

from api.src.models.LXDModule import LXDModule
from api.src.models.LXCProfile import LXCProfile
from api.src.utils import response

profile_api = Blueprint('profile_api', __name__)


@profile_api.route('/')
def profiles():
    client = LXDModule()
    return response.reply(client.listProfiles())


@profile_api.route('/', methods=['POST'])
def create_profile():
    data = request.get_json()
    try:
        profile = LXCProfile(data)
        return jsonify(profile.createProfile())
    except ValueError as ex:
        return response.replyFailed(ex.__str__())


@profile_api.route('/<string:name>')
def get_profile(name):
    profile = LXCProfile({'name': name})
    return response.reply(profile.info())


@profile_api.route('/<string:name>', methods=['DELETE'])
def delete_profile(name):
    profile = LXCProfile({'name': name})
    try:
        profile.deleteProfile()
        return response.reply()
    except ValueError as ex:
        return response.replyFailed(message=ex.__str__())


@profile_api.route('/<string:name>', methods=['PUT'])
def update_profile():
    data = request.get_json()
    profile = LXCProfile(data)
    try:
        return response.reply(profile.updateProfile())
    except ValueError as ex:
        return response.replyFailed(message=ex.__str__())
