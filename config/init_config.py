import os
from config import config


def init_config(env=os.environ.get('FLASK_ENV')):
    if env == 'development':
        return config.Development
    else:
        return config.Production
