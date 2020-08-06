import os
from shutil import make_archive, rmtree
import re
import logging


def get_folder(task_id):
    folder_name = "../content/{0}/".format(task_id)
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    return folder_name


def save_to_file(content, filename):
    filename = re.sub(r"[\\:*?\"<>\|]", "_", filename)
    try:
        with open(filename, 'wb') as f:
            f.write(content)
    except FileNotFoundError as e:
        logging.exception("Exception occurred while saving file")


def archive_folder(folder_name):
    if os.path.exists(folder_name):
        make_archive(folder_name, 'zip', folder_name)
        rmtree(folder_name)
        return folder_name
    else:
        return False


def transform_url(old_url, parent_url=""):
    new_url = old_url
    if new_url.startswith("//"):
        new_url = 'https:{}'.format(new_url)
    if new_url.startswith("/"):
        new_url = '{}{}'.format(parent_url, new_url)

    if not new_url.startswith("http"):
        return None

    return new_url


def check_url(url, base_url):
    return url is not None and url.startswith(base_url)
