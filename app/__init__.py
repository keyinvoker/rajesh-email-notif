from logging import getLogger

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

from app.utils.email_scheduler import start_scheduler

db = SQLAlchemy()
app = Flask("Email Notif")
app.config.from_object(Config)
db.init_app(app)
api = Api(app)
ma = Marshmallow(app)

app_logger = getLogger('app')
error_logger = getLogger('error')

start_scheduler()

from app.routes import *
