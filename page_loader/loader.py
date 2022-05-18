import os
from pathlib import Path
from typing import Union, Optional

from page_loader.file import write
from page_loader.html import update_html
from page_loader.logger import logger_
from page_loader.request import make_request
from page_loader.url import transform_url_to_path


def download_(url: str, path: Union[str, Path]) -> Optional[str]:
    """Download html page located on url and save it to path/url.html"""
    path_to_dir = Path(path)
    if not path_to_dir.exists():
        logger_.error(f'Path {path} does not exist')
        raise FileExistsError(f'Path {path} does not exist')

    if not os.access(path_to_dir, os.W_OK):
        logger_.error(f'Permissions denied to path {path}')
        raise PermissionError(f'Permissions denied to path {path}')

    response = make_request(url)

    html_file_name = transform_url_to_path(url, 'html')
    path_to_html = path_to_dir.joinpath(html_file_name)

    files_dir_name = transform_url_to_path(url, '_files', True)
    path_to_files = path_to_dir.joinpath(files_dir_name)

    if os.path.exists(path_to_files):
        logger_.warning(f'Directory exists: {path_to_files}')
    else:
        os.mkdir(path_to_files)

    html = response.text

    html = update_html(html, path_to_files, url)

    write(path_to_html, html)
    return str(path_to_html.absolute())
