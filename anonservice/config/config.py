
from os import environ, path
from dotenv import load_dotenv
import redis

file_path = path.abspath(path.dirname(__file__))
full_path = path.join(file_path, '../../.env')
load_dotenv(full_path)


class Config(object):
    FLASK_APP = environ.get('FLASK_APP')
    SECRET_KEY = environ.get('FLASK_SECRET')

    # cache
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = environ.get('CACHE_REDIS_HOST') or 'localhost'
    CACHE_REDIS_PORT = environ.get('CACHE_REDIS_PORT') or '6379'
    #CACHE_REDIS_URL = environ.get('CACHE_REDIS_URL')
    CACHE_REDIS_PASSWORD = environ.get('CACHE_REDIS_PASSWORD')
    CACHE_DEFAULT_TIMEOUT = 500000

    # session
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.Redis(
        host=CACHE_REDIS_HOST,
        port=CACHE_REDIS_PORT,
        password=CACHE_REDIS_PASSWORD,
    )

    # auth
    AUTH_ROOT_ENDPOINT = environ.get('AUTH_ROOT_ENDPOINT')
    AUTH_AUDIENCE = 'AnonChat'
    AUTH_REALMS_PATH = AUTH_ROOT_ENDPOINT + '/realms/AnonChat'
    AUTH_CERTS_ENDPOINT = AUTH_ROOT_ENDPOINT + environ.get('AUTH_CERTS_PATH')


class Production(Config):
    DEBUG = False



class Development(Config):
    DEBUG = True


