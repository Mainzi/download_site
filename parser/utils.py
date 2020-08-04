import os
import sqlite3
from shutil import make_archive, rmtree
import re

parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


def get_url_from_db(task_id):
    # TODO: take out connection control
    conn = sqlite3.connect(os.path.join(parent_dir, 'app.db'))
    cursor = conn.cursor()
    sql = "SELECT url, status FROM task where id=?"
    cursor.execute(sql, (task_id, ))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result[1] == "added" else False


def change_task_status(task_id, status):
    # TODO: take out connection control
    conn = sqlite3.connect(os.path.join(parent_dir, 'app.db'))
    cursor = conn.cursor()
    sql = ''' UPDATE task
              SET status = ?
              WHERE id = ?'''
    cursor.execute(sql, (status, task_id,))
    conn.commit()
    conn.close()
    return True


def get_folder_name(task_id):
    folder_name = "content/{0}/".format(task_id)
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    return folder_name


def save_to_file(content, filename):
    filename = re.sub(r"[\\:*?\"<>\|]", "_", filename)
    try:
        with open(filename, 'wb') as f:
            f.write(content)
    except FileNotFoundError as e:
        print(e)


def archive_folder(folder_name):
    if os.path.exists(folder_name):
        make_archive(folder_name, 'zip', folder_name)
        rmtree(folder_name)
        return folder_name
    else:
        return False
