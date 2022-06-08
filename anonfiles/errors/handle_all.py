from anonfiles import socketio as io


class Halt(Exception):

    def __init__(self, code, msg):
        self.code = code
        self.msg = {"error": msg}


@io.on_error_default
def handle_errors(err: Halt, content='application/json'):
    io.emit('error', err.msg)





