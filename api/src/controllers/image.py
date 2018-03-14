from flask import Blueprint, request
from flask_jwt import jwt_required

from api.src.models.LXCImage import LXCImage
from api.src.models.LXDModule import LXDModule
from api.src.utils import response

from api.src.helpers.download_image_schema import doValidate

image_api = Blueprint('image_api', __name__)

@image_api.route('/')
@jwt_required()
def images():
    try:
        client = LXDModule()
        return response.replySuccess(client.listLocalImages())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@image_api.route('/<string:fingerprint>')
@jwt_required()
def image(fingerprint):
    try:
        image = LXCImage({'fingerprint': fingerprint})
        return response.replySuccess(image.getImage())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@image_api.route('/<string:fingerprint>', methods=['DELETE'])
@jwt_required()
def delete(fingerprint):
    try:
        image = LXCImage({'fingerprint': fingerprint})
        return response.replySuccess(image.deleteImage())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@image_api.route('/remote')
@jwt_required()
def remote():
    try:
        client = LXDModule()
        return response.replySuccess(client.listRemoteImages())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())


@image_api.route('/remote', methods=['POST'])
@jwt_required()
def downloadImage():
    input = request.get_json(silent=True)
    validation = doValidate(input)
    if validation:
        return response.replyFailed(message=validation.message)
    try:
        client = LXDModule()
        return response.replySuccess(client.downloadImage(input.get('image')))
    except ValueError as e:
        return response.replyFailed(message=e.__str__())