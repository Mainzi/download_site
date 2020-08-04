from pip._vendor import requests
import re
from bs4 import BeautifulSoup
from utils import get_folder_name, save_to_file, archive_folder


def parse_url(url, task_id):
    print("{0} start parsing".format(url))
    download_data_from_url(url, task_id=task_id)
    archive_folder(get_folder_name(task_id))
    print("{0} parsed".format(url))


def download_data_from_url(url, task_id):
    folder = get_folder_name(task_id)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    base_url = re.search(r'((https|http)://[\w_\-.]+)', url)
    if not base_url:
        return False
    base_url = base_url.group(1)

    with open(folder + task_id + '.html', 'w', encoding='utf-8') as f:
        f.write(response.text)

    download_media(soup, folder, base_url)
    download_js(soup, folder, base_url)
    download_css(soup, folder, base_url)

    return folder


def download_media(parsed_data, folder, base_url):
    # find all jpg, png, gif, svg
    print("Download media")
    links = set([link['href'] for link in parsed_data.findAll('link', href=True)] +
                [img['src'] for img in parsed_data.find_all('img')])
    for link in links:
        print(link)
        filename = re.search(r'/([\w_\-.]+[.](jpg|gif|png|jpeg|svg))$', link)
        link = transform_url(link, base_url)
        if not filename or not link:
            continue

        response = requests.get(link)
        if response.ok:
            save_to_file(response.content, folder + filename.group(1))


def download_js(parsed_data, folder, base_url):
    # find all js
    print("Download JS")
    links = [sc["src"] for sc in parsed_data.find_all("script", src=True)]
    for link in links:
        print(link)
        filename = re.search(r'/([^/]+)$', link)
        link = transform_url(link, base_url)
        if not filename or not link:
            continue

        response = requests.get(link)
        if response.ok:
            save_to_file(response.content, folder + filename.group(1))


def download_css(parsed_data, folder, base_url):
    # find all css
    print("Download CSS")
    links = [link['href'] for link in parsed_data.findAll('link', href=True, rel="stylesheet")]
    for link in links:
        print(link)
        filename = re.search(r'/([^/]+)$', link)
        link = transform_url(link, base_url)
        if not filename or not link:
            continue

        response = requests.get(link)
        if response.ok:
            save_to_file(response.content, folder + filename.group(1))


def transform_url(old_url, parent_url=""):
    new_url = old_url
    if new_url.startswith("//"):
        new_url = 'https:{}'.format(new_url)
    if new_url.startswith("/"):
        new_url = '{}{}'.format(parent_url, new_url)

    if not new_url.startswith("http"):
        return False

    return new_url



