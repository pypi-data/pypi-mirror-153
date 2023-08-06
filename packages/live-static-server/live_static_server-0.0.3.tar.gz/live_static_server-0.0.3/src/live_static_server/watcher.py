from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import tornado.ioloop
import tornado.autoreload

from . import config
from .server.app import broadcast_reload, start_app

app = None
observer = None
loop = None

class LiveServerEventHandler(FileSystemEventHandler):
    def refresh_app():
        global app
        broadcast_reload()

    def on_any_event(self, event):
        global app
        global loop
        print(event)
        loop.add_callback(LiveServerEventHandler.refresh_app)


def watch():
    global observer

    live_server_event_handler = LiveServerEventHandler()
    observer = Observer()
    observer.schedule(live_server_event_handler, config.SERVER_ROOT, recursive=True)
    observer.start()


def main():
    global app
    global loop

    loop = tornado.ioloop.IOLoop.current()
    loop.add_callback(watch)
    app = start_app()
    try:
        loop.start()
    except KeyboardInterrupt:
        print('\nLive Static Server stopped.')
