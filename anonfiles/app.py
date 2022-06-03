import os

from flask import Flask, request
from config.init_config import init_config
from anonfiles import cache, sess, socketio
from dotenv import load_dotenv


def make_app(env_type=os.getenv('FLASK_ENV', None)):
    app = Flask(__name__)
    if env_type == 'development':
        path = os.path.join(__file__, '../.env')
        load_dotenv(path)

    get_config = init_config()
    app.config.from_object(get_config)
    # register blueprints
    reg_blueprints(app)
    sess.init_app(app)
    cache.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    return app


def reg_blueprints(app):
    from anonfiles.rooms.routes import bp
    app.register_blueprint(bp)







