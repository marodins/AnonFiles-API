from flask import Blueprint, request
from anonfiles.errors.handle_all import Halt
from anonfiles import cache, socketio as io

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('join', methods=["GET"])
def try_room():
    pass




