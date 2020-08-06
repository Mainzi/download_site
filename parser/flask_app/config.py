import os

basedir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


class Config(object):
    CONTENT_DIRECTORY = os.path.join(basedir, "content")
    LOG_FILE = os.path.join(basedir, "archive_flask.log")
