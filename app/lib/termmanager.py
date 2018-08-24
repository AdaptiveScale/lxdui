from terminado import TermSocket, TermManagerBase
import signal

from terminado.management import MaxTerminalsReached
from tornado import gen
from tornado.ioloop import IOLoop
import itertools

## Modified version of NamedTermManager
class NamedTermManager(TermManagerBase):
    """Share terminals between websockets connected to the same endpoint.
    """

    def __init__(self, max_terminals=None, **kwargs):
        super(NamedTermManager, self).__init__(**kwargs)
        self.max_terminals = max_terminals
        self.terminals = {}

    def get_terminal(self, term_name, **kwargs):
        assert term_name is not None

        if term_name in self.terminals:
            return self.terminals[term_name]

        if self.max_terminals and len(self.terminals) >= self.max_terminals:
            raise MaxTerminalsReached(self.max_terminals)

        # Create new terminal
        self.log.info("New terminal with specified name: %s", term_name)
        term = self.new_terminal(**kwargs)
        term.term_name = term_name
        self.terminals[term_name] = term
        self.start_reading(term)
        return term

    name_template = "%d"

    def _next_available_name(self):
        for n in itertools.count(start=1):
            name = self.name_template % n
            if name not in self.terminals:
                return name

    def new_named_terminal(self, **kwargs):
        name = self._next_available_name()
        term = self.new_terminal(**kwargs)
        self.log.info("New terminal with automatic name: %s", name)
        term.term_name = name
        self.terminals[name] = term
        self.start_reading(term)
        return name, term

    def kill(self, name, sig=signal.SIGTERM):
        term = self.terminals[name]
        term.kill(sig)  # This should lead to an EOF

    def client_disconnected(self, websocket):
        if (len(self.terminals[websocket.term_name].clients)==0):
            del self.terminals[websocket.term_name]

    @gen.coroutine
    def terminate(self, name, force=False):
        term = self.terminals[name]
        yield term.terminate(force=force)

    def on_eof(self, ptywclients):
        super(NamedTermManager, self).on_eof(ptywclients)
        name = ptywclients.term_name
        self.log.info("Terminal %s closed", name)
        self.terminals.pop(name, None)

    @gen.coroutine
    def kill_all(self):
        yield super(NamedTermManager, self).kill_all()
        self.terminals = {}