import json

from flask import Blueprint, request, redirect, render_template, \
    make_response, url_for
from anonfiles.errors.handle_all import Halt


bp = Blueprint('main', __name__, url_prefix='/',
               static_folder='../../static/build/static',
               template_folder='../../static/build')


@bp.route('', methods=["GET"])
def home():
    print('request')
    return render_template('index.html')

