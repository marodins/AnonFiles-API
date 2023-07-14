import os

from flask import Flask, request
from anonfiles import cache, sess, socketio

from anonfiles.rooms import events
from anonfiles.messages import events


def make_app(env_type=os.getenv('FLASK_ENV', None)):
    app = Flask(__name__, static_folder='../static/build',
                template_folder='../static/build')
    from config.init_config import init_config
    get_config = init_config()
    app.config.from_object(get_config)
    # register blueprints
    reg_blueprints(app)
    sess.init_app(app)
    cache.init_app(app)
    socketio.init_app(app, cors_allowed_origins=[], engineio_logger=True)
    return app


def reg_blueprints(app):
    from anonfiles.rooms.routes import bp
    app.register_blueprint(bp)

