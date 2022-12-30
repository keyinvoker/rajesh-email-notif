import json
import os
from dotenv import find_dotenv, load_dotenv
from logging.config import dictConfig

load_dotenv(find_dotenv())

EMAIL_SENDER = os.environ.get('EMAIL_SENDER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_SERVER = os.environ.get('EMAIL_SERVER')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

MAX = int(os.environ.get('MAX'))
PERIOD = os.environ.get('PERIOD')
CHANGING_DURATION = json.loads(os.environ.get('CHANGING_DURATION'))
CONSTANT_DURATION = int(os.environ.get('CONSTANT_DURATION'))

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_NAME = os.environ.get('DB_NAME')
DB_PASS = os.environ.get('DB_PASS')
DB_CONNECT_STRING = (
    f'postgresql+pg8000://{ DB_USER }:{ DB_PASS }'
    f'@{ DB_HOST }/{ DB_NAME }'
)

BASE_ENDPOINT = os.environ.get('BASE_ENDPOINT')


# NOTE: [Logging]
here = os.path.abspath(os.path.dirname(__file__))


def get_log_filename(log_filename):
    return os.path.join(here, os.pardir, 'app/logs', f'{ log_filename }.log')


LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'file_app': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1000000000,
            'backupCount': 5,
            'level': 'INFO',
            'formatter': 'simple',
            'filename': get_log_filename('app'),
        },
        'file_error': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1000000000,
            'backupCount': 5,
            'level': 'ERROR',
            'formatter': 'simple',
            'filename': get_log_filename('error'),
        },
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'app': {
            'handlers': ['console', 'file_app'],
            'propagate': False,
        },
        'error': {
            'handlers': ['console', 'file_error'],
            'propagate': False,
        },
    },
    'root': {'level': 'INFO', 'handlers': ['console', 'file_error']},
}


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = DB_CONNECT_STRING
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    dictConfig(LOGGING_CONFIG)
