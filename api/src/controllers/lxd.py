from flask import Blueprint, abort
from flask import jsonify

from api.src.models.LXDModule import LXDModule

lxd_api = Blueprint('lxd_api', __name__)

@lxd_api.route('/containers')
def containers():
    client = LXDModule()
    return jsonify({'containers': client.listContainers()})


@lxd_api.route('/images')
def images():
    client = LXDModule()
    return jsonify({'images': client.listLocalImages()})