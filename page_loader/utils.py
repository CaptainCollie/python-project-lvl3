import os
import re
from pathlib import Path
from typing import Union
from urllib.parse import urlparse

import requests

from page_loader.logger import logger_


def transform_url_to_file_name(url: str, postfix: str = '',
                               is_dir: bool = False) -> str:
    """Transforms url to file name
    https://ru.hexlet.io/courses -> ru-hexlet-io-courses.html"""
    parsed_url = urlparse(url)
    default_postfix = ''
    if len(parsed_url.path.split('.')) == 2:
        default_postfix = parsed_url.path.split('.')[-1]
        parsed_url = parsed_url._replace(
            path=''.join(parsed_url.path.split('.')[:-1]))

    if not postfix and not default_postfix:
        postfix = 'html'
    elif not postfix:
        postfix = default_postfix

    if not is_dir:
        postfix = '.' + postfix

    if parsed_url.path == '/':
        parsed_url = parsed_url._replace(path='')
    prepared_ulr = re.sub(rf'{parsed_url.scheme}://', '', parsed_url.geturl())
    file_name = re.sub(r'[^\w\d]', '-', prepared_ulr) + postfix
    return file_name


def create_dir(dir_path):
    try:
        os.mkdir(dir_path)
    except FileExistsError:
        logger_.warning(f'Directory exists: {dir_path}')


def get_response(url):
    logger_.info(f'Request to {url}')
    response = requests.get(url)
    logger_.info(f'Response status {response.status_code}')
    if not response.status_code == 200:
        logger_.error(f'Connection to {url} failed\n'
                      f'{response.status_code}')
        raise ConnectionError(f'Connection to {url} failed\n'
                              f'{response.reason}\n'
                              f'{response.status_code}'
                              )
    return response


def choose_mode(file_txt: Union[str, bytes]) -> str:
    if isinstance(file_txt, bytes):
        return 'wb'
    elif isinstance(file_txt, str):
        return 'w'
    return ''


def write_to_file(path: Union[Path, str], data: Union[str, bytes]) -> None:
    mode = choose_mode(data)
    logger_.info(f'Writing in file {path}')
    with open(path, mode) as f:
        f.write(data)
