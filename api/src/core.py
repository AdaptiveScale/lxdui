from flask import Flask

app = Flask(__name__)

from api.src.controllers.lxd import lxd_api
app.register_blueprint(lxd_api, url_prefix='/api/lxd')

from api.src.controllers.container import container_api
app.register_blueprint(container_api, url_prefix='/api/container')

from api.src.controllers.image import image_api
app.register_blueprint(image_api, url_prefix='/api/image')

@app.cli.command
def run():
    startApp()

def startApp(uiPages=None):
    if uiPages is not None:
        app.register_blueprint(uiPages, url_prefix='/ui')
    else:
        print('ui not included')
    app.run(debug=True, host='0.0.0.0')