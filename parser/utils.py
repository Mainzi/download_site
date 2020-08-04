import os
import sqlite3

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
