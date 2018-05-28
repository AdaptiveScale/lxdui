import os

import tornado
import tornado.web
import tornado.wsgi
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import tornado_xstatic as tornado_xstatic
from terminado import TermSocket
from app.lib.termmanager import NamedTermManager

AUTH_TYPES = ("none", "login")

UI_DIR = os.path.dirname(__file__).replace('/api/controllers','/ui')
TEMPLATE_DIR = UI_DIR+ "/templates/"
STATIC_DIR = UI_DIR+ "/static/"

class TerminalPageHandler(tornado.web.RequestHandler):
    """Render the /ttyX pages"""
    def get(self, term_name):
        return self.render("termpage.html",static=self.static_url,
                           xstatic=self.application.settings['xstatic_url'],
                           ws_url_path="/_websocket/"+term_name)

class NewTerminalHandler(tornado.web.RequestHandler):
    """Redirect to an unused terminal name"""
    def get(self, name='new'):
        shell = ['bash', '-c', 'lxc exec {} -- /bin/bash'.format(name)]
        name, terminal = self.application.settings['term_manager'].new_named_terminal(shell_command=shell)
        self.redirect("/terminal/" + name, permanent=False)

def terminal(app, port):
    term_manager = NamedTermManager(shell_command=None, max_terminals=100)
    wrapped_app = WSGIContainer(app)
    handlers = [
                (r"/_websocket/(\w+)", TermSocket,
                     {'term_manager': term_manager}),
                (r"/terminal/new/([a-zA-Z\-0-9\.]+)/?", NewTerminalHandler),
                (r"/terminal/(\w+)/?", TerminalPageHandler),
                (r"/xstatic/(.*)", tornado_xstatic.XStaticFileHandler),
                ("/(.*)", tornado.web.FallbackHandler, {'fallback': wrapped_app}),
               ]

    tornado_app = tornado.web.Application(handlers, static_path=STATIC_DIR,
                              template_path=TEMPLATE_DIR,
                              xstatic_url=tornado_xstatic.url_maker('/xstatic/'),
                              term_manager=term_manager)
    http_server = HTTPServer(tornado_app)
    http_server.listen(port, '0.0.0.0')
    IOLoop.instance().start()