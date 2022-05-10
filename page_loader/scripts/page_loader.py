#! usr/env/python
import os
import sys
from pathlib import Path
from typing import Union, Optional
from urllib.parse import urlparse

from page_loader.html import replace_links_to_paths
from page_loader.logger import logger_
from page_loader.parse_args import parse_args
from page_loader.utils import transform_url_to_file_name, create_dir, \
    get_response, write_to_file

__all__ = ['download']


def download(url: str, path: Union[str, Path]) -> Optional[str]:
    """Download html page located on url and save it to path/url.html"""
    path_to_dir = Path(path)
    if not path_to_dir.exists():
        logger_.error(f'Path {path} does not exist')
        raise FileExistsError(f'Path {path} does not exist')

    if not os.access(path_to_dir, os.W_OK):
        logger_.error(f'Permissions denied to path {path}')
        raise PermissionError(f'Permissions denied to path {path}')

    response = get_response(url)

    html_file_name = transform_url_to_file_name(url, 'html')
    path_to_html = path_to_dir.joinpath(html_file_name)

    files_dir_name = transform_url_to_file_name(url, '_files', True)
    path_to_files = path_to_dir.joinpath(files_dir_name)

    create_dir(path_to_files)

    html = response.text

    html = replace_links_to_paths(html, path_to_files, url)

    write_to_file(path_to_html, html)
    return str(path_to_html.absolute())


def main():
    args = parse_args(sys.argv[1:])
    file_path = download(args.url, args.output)
    print(f"Page was successfully downloaded into '{file_path}'")


if __name__ == "__main__":
    main()
