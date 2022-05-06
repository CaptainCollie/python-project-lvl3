import logging
import os
import re

from urllib.parse import urlparse


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
        logging.warning(f'Directory exists: {dir_path}')
