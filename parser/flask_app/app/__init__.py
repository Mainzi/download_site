from flask import Flask
import logging
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

logging.basicConfig(filename=app.config["LOG_FILE"])

from app import routes
