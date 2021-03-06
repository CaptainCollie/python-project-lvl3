import os
from pathlib import Path
from typing import List, Optional, Union, Tuple
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from progress.bar import ChargingBar

from page_loader.file import write
from page_loader.scripts import logger_
from page_loader.url import transform_to_path

downloading_triplets = (('img', 'src'),
                        ('link', 'href'),
                        ('script', 'src'))


def gather_data_for_downloading_and_prepare_html(html: str,
                                                 path_to_files: Path,
                                                 url: str) -> Tuple[str, list]:
    data_for_downloading = parse_html(html)
    download_pairs = []
    for sources, attr in data_for_downloading:
        sources_to_download = collect_assets(sources,
                                             attr,
                                             path_to_files,
                                             url)

        for url, path, url_to_replace in sources_to_download:
            download_pairs.append((url, path))
            html = html.replace(url_to_replace, '/'.join(path.parts[3:]))

    return BeautifulSoup(html, 'html.parser').prettify(), download_pairs


def parse_html(html: str) -> list:
    soup = BeautifulSoup(html, 'html.parser')

    result = []
    for tag, attr in downloading_triplets:
        sources = soup.find_all(tag)
        if tag == 'img':
            sources = [src for src in sources if
                       '.png' in src.get(attr) or '.jpg' in src.get(attr)]
        result.append((sources, attr))
    return result


def collect_assets(sources: List[BeautifulSoup],
                   attr: str,
                   full_path_to_files: Path,
                   url: str,
                   extension: str = ''):
    """Downloads source and put them into full_path_to_files
    Returns changed html"""
    parsed_url = urlparse(url)
    base_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
    sources_to_download = []

    for src in sources:
        src_url = src.get(attr)
        parsed_src_url = urlparse(src_url)
        if parsed_src_url.scheme and base_url not in src_url:
            continue

        base_src_url = src_url

        if not parsed_src_url.netloc and parsed_src_url.path.startswith('/'):
            src_url = urljoin(base_url, src_url)
        elif not parsed_src_url.netloc and not parsed_src_url.path.startswith(
                '/'):
            src_url = urljoin(url, src_url)

        path_to_src = transform_to_path(src_url, extension)
        path_to_src = full_path_to_files.joinpath(path_to_src)

        sources_to_download.append((src_url, path_to_src, base_src_url))

    return sources_to_download


def download_sources(download_pairs: List[Tuple[str, str]]):
    for src_url, path_to_src in download_pairs:
        bar = ChargingBar(max=1)
        bar.message = src_url + ' '
        bar.start()

        src_response = make_request(src_url)
        file_txt = src_response.content
        write(path_to_src, file_txt)
        bar.next()
        bar.finish()


def download(url: str, path: Union[str, Path]) -> Optional[str]:
    """Download html page located on url and save it to path/url.html"""
    path_to_dir = Path(path)
    if not path_to_dir.exists():
        raise FileExistsError(f'Path {path} does not exist')

    if not os.access(path_to_dir, os.W_OK):
        raise PermissionError(f'Permissions denied to path {path}')

    response = make_request(url)

    html_file_name = transform_to_path(url, '.html')
    path_to_html = path_to_dir.joinpath(html_file_name)

    files_dir_name = transform_to_path(url, is_dir=True)
    path_to_files = path_to_dir.joinpath(files_dir_name)

    if not os.path.exists(path_to_files):
        os.mkdir(path_to_files)
        logger_.warning(f'Directory created: {path_to_files}')

    html = response.text

    html, download_triplets = gather_data_for_downloading_and_prepare_html(
        html, path_to_files, url)
    download_sources(download_triplets)

    write(path_to_html, html)
    return str(path_to_html.absolute())


def make_request(url):
    logger_.info(f'Request to {url}')
    response = requests.get(url)
    logger_.info(f'Response status {response.status_code}')
    response.raise_for_status()
    return response
