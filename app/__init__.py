from logging import getLogger

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

db = SQLAlchemy()
app = Flask("Email Notif")
app.config.from_object(Config)
db.init_app(app)
api = Api(app)
ma = Marshmallow(app)

app_logger = getLogger('app')
error_logger = getLogger('error')

from app.routes import *
from app.utils import email_scheduler
