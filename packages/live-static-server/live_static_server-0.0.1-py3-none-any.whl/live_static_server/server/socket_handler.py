from tornado.websocket import WebSocketHandler


class SocketHandler(WebSocketHandler):
    active_clients = set()

    def open(self):
        SocketHandler.active_clients.add(self)

    def on_close(self):
        SocketHandler.active_clients.remove(self)
