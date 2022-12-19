from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())

EMAIL_SENDER = os.environ.get('EMAIL_SENDER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_SERVER = os.environ.get('EMAIL_SERVER')
EMAIL_PORT = os.environ.get('EMAIL_PORT')

PERIOD = os.environ.get('PERIOD')
MAX = os.environ.get('MAX')

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_NAME = os.environ.get('DB_NAME')
DB_PASS = os.environ.get('DB_PASS')
DB_CONNECT_STRING = (
    f'postgresql+pg8000://{ DB_USER }:{ DB_PASS }@'
    f'{ DB_HOST }/{ DB_NAME }'
)

ENDPOINT = os.environ.get('ENDPOINT')
