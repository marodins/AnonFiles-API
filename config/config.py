
from os import environ, path
from dotenv import load_dotenv
import redis

file_path = path.abspath(path.dirname(__file__))
full_path = path.join(file_path, '../.env')
load_dotenv(full_path)


class Config(object):
    FLASK_APP = environ.get('FLASK_APP')
    SECRET_KEY = environ.get('FLASK_SECRET')

    # cache
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = environ.get('CACHE_REDIS_HOST')
    CACHE_REDIS_PORT = environ.get('CACHE_REDIS_PORT')
    CACHE_REDIS_URL = environ.get('CACHE_REDIS_URL')
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
    AUTH0_CLIENT_ID = environ.get('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = environ.get('AUTH0_CLIENT_SECRET')
    AUTH0_DOMAIN = environ.get('AUTH0_DOMAIN')
    AUTH0_AUDIENCE = environ.get('AUTH0_AUDIENCE')
    AUTH0_CONNECTION = environ.get('CONNECTION')
    AUTH0_SERVER_METADATA_URL = environ.get('AUTH0_SERVER_METADATA_URL')
    AUTH0_NAME = "auth0"
    AUTH0_ACCESS_TOKEN_URL = f'https://{AUTH0_DOMAIN}/oauth/token'
    AUTH0_API_BASE_URL = f'https://{AUTH0_DOMAIN}'


class Production(Config):
    DEBUG = False
    PREFERRED_URL_SCHEME = 'https'


class Development(Config):
    DEBUG = True


