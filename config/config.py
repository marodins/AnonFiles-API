from os import environ
import redis


class Config(object):
    FLASK_APP = environ.get('FLASK_APP')
    SECRET_KEY = environ.get('FLASK_SECRET')

    # session
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True

    # cache
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = environ.get('CACHE_REDIS_HOST')
    CACHE_REDIS_PORT = environ.get('CACHE_REDIS_PORT')
    CACHE_REDIS_URL = environ.get('CACHE_REDIS_URL')
    CACHE_DEFAULT_TIMEOUT=50000

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
    FLASK_ENV = 'production'


class Development(Config):
    DEBUG = True
    FLASK_ENV = 'development'
    SESSION_REDIS = redis.from_url(environ.get('SESSION_REDIS'))

