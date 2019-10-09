import os

import tornado
import tornado.web
import tornado.wsgi
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import tornado_xstatic as tornado_xstatic
from terminado import TermSocket

from app.api.models.LXCContainer import LXCContainer
from app.lib.termmanager import NamedTermManager
from app.api.utils import mappings

TEMPLATE_DIR = os.path.dirname(__file__).replace('/api/controllers','/ui/templates/')
STATIC_DIR = os.path.dirname(__file__).replace('/api/controllers','/ui/static/')

from app.api.utils.authentication import jwt_decode_handler

def findShellTypeOfContainer(container):
    containerImage = container.info()['config'].get('image.os')
    if containerImage:
        for image in mappings.OS_SHELL_MAPPINGS:
            if image in containerImage.lower():
                return mappings.OS_SHELL_MAPPINGS[image]
    return 'bash'

def checkAuthentication(token):
    try:
        return jwt_decode_handler(token)
    except Exception as e:
        return False

class TerminalPageHandler(tornado.web.RequestHandler):
    """Render the /ttyX pages"""
    def get(self, term_name, token):
        if not checkAuthentication(token):
            raise tornado.web.HTTPError(403)
        return self.render("termpage.html",static=self.static_url,
                           xstatic=self.application.settings['xstatic_url'],
                           ws_url_path="/_websocket/"+term_name)

class NewTerminalHandler(tornado.web.RequestHandler):
    """Redirect to an unused terminal name"""
    def get(self, name='new', token=None):
        if not checkAuthentication(token):
            raise tornado.web.HTTPError(403)
        shellType = findShellTypeOfContainer(LXCContainer({'name': name}))
        shell = ['bash', '-c', 'lxc exec {} -- /bin/{}'.format(name, shellType)]
        name, terminal = self.application.settings['term_manager'].new_named_terminal(shell_command=shell)
        self.redirect("/terminal/open/" + name+'/'+token, permanent=False)

def terminal(app, host, port, debug=False):
    term_manager = NamedTermManager(shell_command=None, max_terminals=100)
    wrapped_app = WSGIContainer(app)
    handlers = [
                (r"/_websocket/(\w+)", TermSocket,
                     {'term_manager': term_manager}),
                (r"/terminal/new/([a-zA-Z\-0-9\.]+)/(.*)/?", NewTerminalHandler),
                (r"/terminal/open/([a-zA-Z\-0-9\.]+)/(.*)/?", TerminalPageHandler),
                (r"/xstatic/(.*)", tornado_xstatic.XStaticFileHandler),
                ("/(.*)", tornado.web.FallbackHandler, {'fallback': wrapped_app}),
               ]

    tornado_app = tornado.web.Application(handlers, static_path=STATIC_DIR,
                              template_path=TEMPLATE_DIR,
                              xstatic_url=tornado_xstatic.url_maker('/xstatic/'),
                              term_manager=term_manager,
                              debug=debug)
    http_server = HTTPServer(tornado_app)
    http_server.listen(port, host)
    IOLoop.instance().start()