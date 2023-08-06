from flask_socketio import SocketIO, Namespace

from .sock import Sock


class SockHandler(Namespace):
    def __init__(self, namespace=None):
        super().__init__(namespace)
        self.sock: Sock = Sock.instance()

    def on_connect(self):
        self.sock.send('Connected')

    def on_disconnect(self):
        self.sock.send('Disconnected')

    def on_message(self, message):
        self.sock.send(f'Hello {message}!')
