import time

from flask import Flask, redirect
from app.api.utils.authentication import initAuth
from app.api.utils.readInstanceDetails import readInstanceDetails
from app.lib.log import Log
from app import __metadata__ as meta
import os
import signal
import tempfile
import psutil
import logging

Log(__name__)
app = Flask(__name__)
HAS_UI = False
PID = os.path.join(tempfile.gettempdir(), '{}.pid'.format(meta.APP_NAME).lower())

# Authentication section
initAuth(app)

from app.api.controllers.auth import auth_api
app.register_blueprint(auth_api, url_prefix='/api/user')

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

from app.api.controllers.fileManager import file_manager_api
app.register_blueprint(file_manager_api, url_prefix='/api/file')

from app.api.controllers.storagePool import storage_pool_api
app.register_blueprint(storage_pool_api, url_prefix='/api/storage_pool')

from app.api.controllers.imageRegistry import image_registry_api
app.register_blueprint(image_registry_api, url_prefix='/api/image_registry')

from app.api.controllers.terminal import terminal

@app.route('/')
def index():
    if HAS_UI:
        return redirect('/ui')
    else:
        return redirect('/api/lxd/config')

@app.cli.command
def run():
    start()

def getPID():
    try:
        with open(PID, 'r') as f:
            pid = int(f.read())
        return pid
    except FileNotFoundError as e:
        logging.info(e)

def status():

    # def _find_proc(name):
    #     "Return a list of processes matching 'app_name'."
    #     ls = []
    #     for p in psutil.process_iter(attrs=["name", "exe", "cmdline"]):
    #         if name == p.info['name'] or \
    #                 p.info['exe'] and os.path.basename(p.info['exe']) == name or \
    #                 p.info['cmdline'] and p.info['cmdline'][0] == name:
    #             ls.append(p)
    #     return ls


    try:
        pid = getPID()
        if pid:
            p = psutil.Process(pid)
            stat = {'running': p.is_running(),
                    'pid': p.pid,
                    'started': time.ctime(p.create_time()),
                    'cmd': p.cmdline(),
                    'cwd': p.cwd(),
                    'ram': p.memory_info(),
                    'connections': p.connections()
                   }
            return stat
        else:
            return 'STOPPED'
    except psutil.NoSuchProcess:
        print('No running process found.')


def stop():
    logging.debug('Stopping the app...')
    try:
        pid = getPID()
        if pid:
            os.kill(pid, signal.SIGTERM)
            os.remove(PID)
            logging.info('Deleting PID file.')
            print('Process terminated.')
        else:
            print('{} is already stopped.'.format(meta.APP_NAME))
            logging.info('no matching process found.')
    except ProcessLookupError as e:
        logging.info(e)


def start(host, port, debug=False, uiPages=None):
    logging.debug('Checking UI availability.')

    if uiPages is not None:
        app.register_blueprint(uiPages, url_prefix='/ui')
        global HAS_UI
        HAS_UI = True
        logging.info('UI Loaded.')
    else:
        logging.warning('UI Missing... Starting without UI.')

    readInstanceDetails()

    pid = os.getpid()
    logging.info('pid={}, pid_file={}'.format(pid, PID))
    with open(PID, 'w') as f:
        f.write(str(pid))

    print("LXDUI started. Running on http://{}:{}".format(host, port))
    print("PID={}, Press CTRL+C to quit".format(pid))
    terminal(app, host, port, debug)
    # app.run(debug=debug, host='0.0.0.0', port=port)
