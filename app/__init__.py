from flask import Flask
import logging
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

logging.basicConfig(filename=app.config["LOG_FILE"])

from app import routes, models