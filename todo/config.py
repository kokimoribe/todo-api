"""Set config values"""

import os

DATABASE_URL = os.environ.get('DATABASE_URL')
DEBUG = os.environ.get('DEBUG', False)
HOST = os.environ.get('HOST', 'localhost:9090')


if not DATABASE_URL:
    raise Exception('Please set `DATABASE_URL` environment variable.')
