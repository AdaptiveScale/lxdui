from flask import Blueprint, request, send_file
from flask_jwt_extended import jwt_required

from app.api.models.LXCImage import LXCImage
from app.api.utils import response

from app.api.schemas.publishImageSchema import doValidate

image_registry_api = Blueprint('image_registry_api', __name__)


@image_registry_api.route('/<string:fingerprint>', methods=['POST'])
@jwt_required()
def publishImage(fingerprint):
    input = request.get_json(silent=True)
    validation = doValidate(input)
    if validation:
        return response.replyFailed(message=validation.message)

    input['fingerprint'] = fingerprint
    try:
        image = LXCImage({'fingerprint': fingerprint})

        #Export Image - Image registry
        image.exportImage(input)

        return response.replySuccess(image.getImage())
    except ValueError as e:
        return response.replyFailed(message=e.__str__())
