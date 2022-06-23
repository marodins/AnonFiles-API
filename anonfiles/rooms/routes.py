import json

from flask import Blueprint, request, redirect, render_template, \
    make_response, url_for
from anonfiles.errors.handle_all import Halt
from anonfiles import cache, socketio as io, auth

bp = Blueprint('main', __name__, url_prefix='/',
               static_folder='../../../AnonFiles-FE/anon-files/build/static/',
               template_folder='../../../AnonFiles-FE/anon-files/build/')


@bp.route('', methods=["GET"])
def home():
    print('in auth')
    return render_template('index.html')


@bp.route('authorize', methods=["GET"])
def try_authorize():
    print('in auth')
    auth0 = auth.create_client('auth0')

    return auth0.authorize_redirect(
        redirect_uri=url_for('main.profile', _external=True)
    )


@bp.route('profile', methods=["GET"])
def profile():
    res = make_response(render_template('index.html'))
    res.set_cookie('token_id', '12345')
    return res


