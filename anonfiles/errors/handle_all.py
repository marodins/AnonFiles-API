from anonfiles import socketio as io
from flask_socketio import emit


class Halt(Exception):

    def __init__(self, code, msg):
        self.code = code
        self.msg = {"error": msg}


@io.on_error_default
def handle_errors(err: Halt):
    emit('error', err.msg)





