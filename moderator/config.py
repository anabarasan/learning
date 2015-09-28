import os
import logging

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

class Config(object):
    APP_DIR = os.path.dirname(os.path.realpath(__file__))
    DATABASE_URI = 'sqlite:///%s' % os.path.join(APP_DIR, 'moderator.sqlite')
    MIGRATE_REPO = os.path.join(APP_DIR, 'db_migration')
    SECRET_KEY = 'secret'
    ADMIN_PASSWORD = 'secret'
    LOG_LEVEL = DEBUG
    DEBUG = False


class DevConfig(Config):
    DEBUG = True
