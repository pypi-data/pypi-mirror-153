import imp
import queue
import eventlet
from multiprocessing import Queue
from os import path
import socketio


def background_loop(q: Queue, sio: socketio.Server):
    while True:
        try:
            while not q.empty():
                event, data = q.get()
                sio.emit(event, data)
        except queue.Empty:
            pass
        eventlet.sleep(0.02)


def run_server(q: Queue, host: str, port: int):
    # specifying just local path breaks when run as a module
    root_path = path.abspath(path.dirname(__file__))
    static_files = {
        '/': {'content_type': 'text/html', 'filename': path.join(root_path, 'index.html')},
        '/static': path.join(root_path, 'static'),
    }

    sio = socketio.Server()
    app = socketio.WSGIApp(sio, static_files=static_files)
    eventlet.spawn(background_loop, q, sio)
    eventlet.wsgi.server(eventlet.listen((host, port)), app)
