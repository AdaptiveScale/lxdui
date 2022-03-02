from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.api.utils.authentication import authenticate

auth_api = Blueprint('auth_api', __name__)

@auth_api.route('/login', methods=['POST'])
def login():
    username = request.get_json()["username"]
    password = request.get_json()["password"]
    auth_resp = authenticate(username,password)
    if auth_resp == False:
      return jsonify('{description: "Invalid credentials", error: "Bad Request", status_code: 401}'), 401
    else:
      access_token = create_access_token(identity = username)
      return '{ "access_token": "'+access_token+'" }'

@auth_api.route('/refresh', methods=['POST'])
@jwt_required()
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return '{ "access_token": "'+access_token+'" }'
