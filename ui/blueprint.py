from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

uiPages = Blueprint('uiPages', __name__,
                        template_folder='src')

@uiPages.route('/', defaults={'page': 'index'})
@uiPages.route('/<page>')
def show(page):
    try:
        return render_template('%s.html' % page)
    except TemplateNotFound:
        abort(404)