import os
from config import config


def init_config(env=os.environ.get('FLASK_DEBUG')):
    if env:
        return config.Development
    else:
        return config.Production
