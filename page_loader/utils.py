import re
from pathlib import Path
from typing import List
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup


def transform_url_to_file_name(url: str, postfix: str) -> str:
    """Transforms url to file name
    https://ru.hexlet.io/courses -> ru-hexlet-io-courses.html"""
    parsed_url = urlparse(url)
    if len(parsed_url.path.split('.')) == 2:
        parsed_url = parsed_url._replace(
            path=''.join(parsed_url.path.split('.')[:-1]))

    if parsed_url.path == '/':
        parsed_url = parsed_url._replace(path='')
    prepared_ulr = re.sub(rf'{parsed_url.scheme}://', '', parsed_url.geturl())
    file_name = re.sub(r'[^\w\d]', '-', prepared_ulr) + postfix
    return file_name


def download_images(images: List[BeautifulSoup], full_path_to_files: Path,
                    base_url: str, html: str) -> str:
    """Downloads images and put them into full_path_to_files
    Returns changed html"""
    for image in images:
        image_url = image.get('src')
        base_image_url = image_url
        if not image_url.startswith('http'):
            image_url = urljoin(base_url, image_url)

        path_to_image = transform_url_to_file_name(image_url, '.png')
        path_to_image = full_path_to_files.joinpath(path_to_image)
        html = html.replace(base_image_url, '/'.join(path_to_image.parts[1:]))
        print('here')
        image_response = requests.get(image_url)
        print('here1')
        with open(path_to_image, 'wb') as f:
            f.write(image_response.content)
        print('OK', image_url)
    return html
