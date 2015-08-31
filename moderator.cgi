#!/usr/bin/python
from wsgiref.handlers import CGIHandler
from moderator import app

CGIHandler().run(app)
