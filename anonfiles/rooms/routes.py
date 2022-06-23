import json

from flask import Blueprint, request, redirect, render_template, \
    make_response, url_for
from authlib.integrations.base_client.errors import MismatchingStateError
from anonfiles.errors.handle_all import Halt
from anonfiles import cache, socketio as io, auth

bp = Blueprint('main', __name__, url_prefix='/',
               static_folder='../../../AnonFiles-FE/anon-files/build/static/',
               template_folder='../../../AnonFiles-FE/anon-files/build/')


@bp.route('', methods=["GET"])
def home():
    print('in auth')
    if request.args.get('code', None):
        return rooms()
    return render_template('index.html')


def rooms():
    try:
        token = auth.auth0.authorize_access_token()
        token.pop('access_token', None)
    except MismatchingStateError:
        return render_template('index.html')
    print(token)
    res = make_response(render_template('index.html'))
    res.set_cookie('token_id', token.get('id_token', None))
    return res


@bp.route('authorize', methods=["GET"])
def try_authorize():
    print('in auth')
    auth0 = auth.create_client('auth0')
    return auth0.authorize_redirect(
        redirect_uri=url_for('main.home', _external=True)
    )




