from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config.from_object('learning.config.DevConfig')

Base = declarative_base()
engine = create_engine(app.config['DATABASE_URI'])

from learning import views, models

Base.metadata.create_all(engine)
Base.metadata.bind = engine
