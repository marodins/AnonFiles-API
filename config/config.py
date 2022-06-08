from os import environ
import redis


class Config(object):
    FLASK_APP = environ.get('FLASK_APP')
    SECRET_KEY = environ.get('SECRET_KEY')

    # session
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True

    # cache
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = environ.get('CACHE_REDIS_HOST')
    CACHE_REDIS_PORT = environ.get('CACHE_REDIS_PORT')
    CACHE_REDIS_URL = environ.get('CACHE_REDIS_URL')


class Production(Config):
    DEBUG = False
    FLASK_ENV = 'production'


class Development(Config):
    DEBUG = True
    FLASK_ENV = 'development'
    SESSION_REDIS = redis.from_url(environ.get('SESSION_REDIS'))

