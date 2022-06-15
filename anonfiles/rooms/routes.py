import json

from flask import Blueprint, request, redirect, render_template, make_response
from anonfiles.errors.handle_all import Halt
from anonfiles import cache, socketio as io

bp = Blueprint('main', __name__, url_prefix='/',
               static_folder='../../../AnonFiles-FE/anon-files/build/static/',
               template_folder='../../../AnonFiles-FE/anon-files/build/')


@bp.route('', methods=["GET"])
def home():
    print('in auth')
    res = make_response(render_template('index.html'))
    res.set_cookie('token_id', '12345')
    return res


@bp.route('authorize', methods=["GET"])
def try_authorize():
    print('in auth')
    return render_template('index.html')





