from flask import send_from_directory, abort
from app import app
import logging


@app.route('/')
@app.route('/index')
def index():
    return "Hello"


@app.route('/get-archive/<string:archive_id>')
def test(archive_id):
    logging.info(f"Sending archive {archive_id}")
    return send_from_directory(app.config["CONTENT_DIRECTORY"], filename=f"{archive_id}.zip")
