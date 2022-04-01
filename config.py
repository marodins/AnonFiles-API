from os import environ
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    SESS_SECRET = environ.get('SESS_SECRET')


class Production(Config):
    DEBUG = False
    FLASK_ENV = 'production'


class Development(Config):
    DEBUG = True
    FLASK_ENV = 'development'

