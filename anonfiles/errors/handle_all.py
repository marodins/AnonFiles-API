from flask import Response, jsonify


class Halt(Exception):

    def __init__(self, code, msg):
        self.code = code
        self.msg = {"error": msg}


def handle_errors(err: Halt, content='application/json'):
    res = Response()
    res.data = jsonify(err.msg)
    res.status_code = err.msg
    res.content_type = content
    return res




