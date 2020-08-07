from bs4.dammit import EncodingDetector
from pip._vendor import requests
import re
from bs4 import BeautifulSoup
from utils import get_folder, save_to_file, archive_folder, transform_url, check_url
import logging


def parse_url(url, task_id):
    logging.info(f'Start parsing {url}')
    folder_name = download_data_from_url(url, task_id=task_id)
    logging.info(f'Try save archive {folder_name}')
    archive_folder(folder_name)
    logging.info(f'End parsing {url}')


def download_data_from_url(url, task_id, base_url=None, depth=1):
    folder = get_folder(task_id)
    if base_url is None:
        base_url = re.search(r'((https|http)://[\w_\-.]+)', url)
        if not base_url:
            raise requests.exceptions.InvalidURL(f"This is not a valid URL: {url}")
        base_url = base_url.group(1)

    response = requests.get(url)

    http_encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(response.content, is_html=True)
    encoding = html_encoding or http_encoding
    soup = BeautifulSoup(response.content, from_encoding=encoding)

    with open(folder + 'index.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    download_media(soup, folder, base_url)
    download_js(soup, folder, base_url)
    download_css(soup, folder, base_url)

    if depth > 0:
        links = set(map(lambda x: transform_url(x, base_url), find_another_urls(soup)))
        for i, link in enumerate(filter(lambda x: check_url(x, base_url), links)):
            try:
                download_data_from_url(link, "{0}/{1}".format(task_id, i), base_url=base_url, depth=depth - 1)
            except requests.exceptions.RequestException as e:
                logging.error(f'Exception occurred while request to {url}\n {e}')
    return folder


def download_media(parsed_data, folder, base_url):
    # find all jpg, png, gif, svg
    links = set([link['href'] for link in parsed_data.findAll('link', href=True)] +
                [img['src'] for img in parsed_data.find_all('img', src=True)])
    for link in links:
        filename = re.search(r'/([\w_\-.]+[.](jpg|gif|png|jpeg|svg))$', link)
        link = transform_url(link, base_url)
        if not filename or link is None:
            continue

        response = requests.get(link)
        if response.ok:
            save_to_file(response.content, folder + filename.group(1))


def download_js(parsed_data, folder, base_url):
    # find all js
    links = [sc["src"] for sc in parsed_data.find_all("script", src=True)]
    for link in links:
        filename = re.search(r'/([^/]+)$', link)
        link = transform_url(link, base_url)
        if not filename or link is None:
            continue

        response = requests.get(link)
        if response.ok:
            save_to_file(response.content, folder + filename.group(1))


def download_css(parsed_data, folder, base_url):
    # find all css
    links = [link['href'] for link in parsed_data.findAll('link', href=True, rel="stylesheet")]
    for link in links:
        filename = re.search(r'/([^/]+)$', link)
        link = transform_url(link, base_url)
        if not filename or link is None:
            continue

        response = requests.get(link)
        if response.ok:
            save_to_file(response.content, folder + filename.group(1))


def find_another_urls(parsed_data):
    return [link['href'] for link in parsed_data.find_all('a', href=True)]
