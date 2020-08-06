import os
import sqlite3
from shutil import make_archive, rmtree
import logging
import sqlalchemy
import config as cfg

engine = sqlalchemy.create_engine(cfg.SQLALCHEMY_DATABASE_URI, client_encoding='utf8')


def get_url_from_db(task_id):
    sql = f"SELECT url, status FROM task where id='{task_id}'"
    with engine.connect() as conn:
        result = list(conn.execute("SELECT url, status FROM task"))
        logging.info(f"ALL {result}")

        result = list(conn.execute(sql))
        if len(result) > 0:
            return result[0][0] if result[0][1] == "added" else False
        else:
            return False


def change_task_status(task_id, status):
    sql = f''' UPDATE task
              SET status = '{status}'
              WHERE id = '{task_id}'
            '''
    with engine.connect() as conn:
        conn.execute(sql)
    return True
