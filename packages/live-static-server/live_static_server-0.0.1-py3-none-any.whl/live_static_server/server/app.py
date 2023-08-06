import os
import tornado.web
import tornado.ioloop

from .. import config
from .html_handler import HtmlHandler
from .socket_handler import SocketHandler


def broadcast_reload():
    for client in SocketHandler.active_clients:
        client.write_message('reload', binary=False)


def make_app():
    static_config = {'path': config.SERVER_ROOT, 'default_filename': 'index.html'}
    app_config = { 'debug': True, 'serve_traceback': True }

    return tornado.web.Application([
        (r'/(.*\.html)?', HtmlHandler, static_config),
        (r'/ws/socket', SocketHandler),
        (r'/(live-static-server.js)', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'static')}),
        (r'/(.*)', tornado.web.StaticFileHandler, static_config)
    ], **app_config)


def start_app():
    app = make_app()
    server = app.listen(config.SERVER_PORT)
    print('listening on {}'.format(config.SERVER_PORT))
    tornado.ioloop.IOLoop.current().start()

    return server


def stop_app(app):
    app.stop()
