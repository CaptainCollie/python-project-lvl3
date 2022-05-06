#! usr/env/python
import os
from pathlib import Path
from typing import List
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from page_loader.parse_args import parse_args
from page_loader.utils import transform_url_to_file_name, download_images

__all__ = ['download']


def download(url, path):
    """Download html page located on url and save it to path/url.html"""
    path_to_dir = Path(path)
    if not path_to_dir.exists():
        raise IOError(f'Path {path} does not exist')

    response = requests.get(url)
    if not response.status_code == 200:
        raise ConnectionError(
            f'Connection to {url} failed\n'
            f'{response.status_code}'
        )

    path_to_html = transform_url_to_file_name(url, '.html')
    path_to_html = path_to_dir.joinpath(path_to_html)

    path_to_files = transform_url_to_file_name(url, '_files')
    path_to_files = path_to_dir.joinpath(path_to_files)
    try:
        os.mkdir(path_to_files)
    except FileExistsError:
        print('File exists.')
    html = response.text

    parsed_url = urlparse(url)
    base_url = f'{parsed_url.scheme}://{parsed_url.netloc}'

    soup = BeautifulSoup(response.text, 'lxml')
    images: List[BeautifulSoup] = soup.find_all('img')
    if images:
        html = download_images(images, path_to_files, base_url, html)

    with open(path_to_html, 'w', encoding='utf-8') as f:
        f.write(html)
    return path_to_html.absolute()


def main():
    args = parse_args()
    file_path = download(args.url, args.output)
    print(file_path)


if __name__ == "__main__":
    main()
