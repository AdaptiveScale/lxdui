from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from api.src.models.LXCContainer import LXDModule, LXCContainer;

uiPages = Blueprint('uiPages', __name__,
                        template_folder='src/templates', static_folder='src/static')

@uiPages.route('/')
def index():
    try:
        containers = LXDModule().listContainers()
        return render_template('containers.html', currentpage=containers)
    except:
        abort(404)