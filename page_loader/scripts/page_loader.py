#! usr/env/python
import os
import sys
from pathlib import Path
from typing import Union
from urllib.parse import urlparse

import requests

from page_loader.html import replace_links_to_paths
from page_loader.parse_args import parse_args
from page_loader.utils import transform_url_to_file_name

__all__ = ['download']


def download(url: str, path: Union[str, Path]) -> str:
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

    html_file_name = transform_url_to_file_name(url, 'html')
    path_to_html = path_to_dir.joinpath(html_file_name)

    files_dir_name = transform_url_to_file_name(url, '_files', True)
    path_to_files = path_to_dir.joinpath(files_dir_name)

    try:
        os.mkdir(path_to_files)
    except FileExistsError:
        print('Directory exists.')
    html = response.text

    parsed_url = urlparse(url)
    base_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
    html = replace_links_to_paths(html, path_to_files, base_url)

    with open(path_to_html, 'w', encoding='utf-8') as f:
        f.write(html)
    return str(path_to_html.absolute())


def main():
    args = parse_args(sys.argv[1:])
    file_path = download(args.url, args.output)
    print(file_path)


if __name__ == "__main__":
    main()