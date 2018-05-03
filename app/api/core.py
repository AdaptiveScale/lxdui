from flask import Flask, redirect

from app.api.utils.authentication import initAuth

from app.lib.log import Log
import logging

Log(__name__)
app = Flask(__name__)
HAS_UI = False

# Authentication section
initAuth(app)

from app.api.controllers.lxd import lxd_api
app.register_blueprint(lxd_api, url_prefix='/api/lxd')

from app.api.controllers.container import container_api
app.register_blueprint(container_api, url_prefix='/api/container')

from app.api.controllers.image import image_api
app.register_blueprint(image_api, url_prefix='/api/image')

from app.api.controllers.profile import profile_api
app.register_blueprint(profile_api, url_prefix='/api/profile')

from app.api.controllers.network import network_api
app.register_blueprint(network_api, url_prefix='/api/network')

from app.api.controllers.snapshot import snapshot_api
app.register_blueprint(snapshot_api, url_prefix='/api/snapshot')

@app.route('/')
def index():
    if HAS_UI:
        return redirect('/ui')
    else:
        return redirect('/api/lxd/config')

@app.cli.command
def run():
    startApp()

def stop():
    app.shutdown()

def startApp(port, uiPages=None):
    logging.debug('Checking ui availability')
    if uiPages is not None:
        app.register_blueprint(uiPages, url_prefix='/ui')
        global HAS_UI
        HAS_UI = True
        logging.info('UI Loaded')
    else:
        logging.warning('UI Missing... Starting without UI.')
    app.run(debug=True, host='0.0.0.0', port=port)