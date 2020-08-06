import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
    POSTGRES_DB = os.environ.get('POSTGRES_DB')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT')

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'  # flask-wtf
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CONTENT_DIRECTORY = os.path.join(basedir, "parser\\content")
    LOG_FILE = os.path.join(basedir, "flask.log")
