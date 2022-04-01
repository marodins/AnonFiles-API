from os import environ
from dotenv import load_dotenv
import redis

load_dotenv()


class Config(object):
    FLASK_APP = environ.get('FLASK_APP')
    SECRET_KEY = environ.get('SECRET_KEY')
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True


class Production(Config):
    DEBUG = False
    FLASK_ENV = 'production'


class Development(Config):
    DEBUG = True
    FLASK_ENV = 'development'
    SESSION_REDIS = redis.from_url(environ.get('SESSION_REDIS'))

