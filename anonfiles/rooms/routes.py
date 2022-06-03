from flask import Blueprint, request
from anonfiles import cache, socketio as io

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('join')
def try_room():
    data = request.args.get
    password = None if data("name") is None else cache.get(data("name"))
    if password is None or data("password") is None:
        return {"reason": "incorrect password or room"}

    if data("password") == password:
        #io.emit()
        #io.join_room(data("name"))
        io.emit("joined")



