from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import logging
import logging.handlers

app = Flask(__name__)
app.config.from_object('moderator.config.DevConfig')

logging.basicConfig(level = app.config['LOG_LEVEL'],
                    filename = app.config['APP_DIR'] + '/moderator.log',
                    format='%(asctime)-15s %(name)-5s %(levelname)-8s %(message)s')

Base = declarative_base()
engine = create_engine(app.config['DATABASE_URI'])

from moderator import views, models

Base.metadata.create_all(engine)
Base.metadata.bind = engine

