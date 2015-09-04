import os


class Config(object):
    DEBUG = False
    APP_DIR = os.path.dirname(os.path.realpath(__file__))
    DATABASE_URI = 'sqlite:///%s' % os.path.join(APP_DIR, 'moderator.sqlite')
    MIGRATE_REPO = os.path.join(APP_DIR, 'db_migration')
    SECRET_KEY = 'secret'
    ADMIN_PASSWORD = 'secret'


class DevConfig(Config):
    DEBUG = True
