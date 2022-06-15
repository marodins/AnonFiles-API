import os

from flask import Flask, request
from anonfiles import cache, sess, socketio
from dotenv import load_dotenv
from flask_cors import CORS
from anonfiles.rooms import events
from anonfiles.messages import events


def make_app(env_type=os.getenv('FLASK_ENV', None)):
    app = Flask(__name__,
                static_folder='../../AnonFiles-FE/anon-files/public/')
    CORS(app, origins=["http://localhost:3000"])
    file_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(file_path, '../.env')
    load_dotenv(path)

    from config.init_config import init_config
    get_config = init_config()
    app.config.from_object(get_config)
    # register blueprints
    reg_blueprints(app)
    #reg_error_handlers(app)
    sess.init_app(app)
    cache.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    return app


def reg_blueprints(app):
    from anonfiles.rooms.routes import bp
    app.register_blueprint(bp)
    #pass


def reg_error_handlers(app):
    #from anonfiles.errors.handle_all import handle_errors, Halt
    #app.register_error_handler(Halt, handle_errors)
    pass






