from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from app.config import DB_CONNECT_STRING

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONNECT_STRING
db = SQLAlchemy(app)
ma = Marshmallow(app)
