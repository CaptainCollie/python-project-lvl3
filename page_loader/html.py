from pathlib import Path
from typing import List
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from page_loader.utils import transform_url_to_file_name, get_response, \
    write_to_file


def replace_links_to_paths(html: str, path_to_files: Path,
                           url: str) -> str:
    soup = BeautifulSoup(html, 'lxml')
    for tag, attr, resp_attr, ext in (
            ('img', 'src', 'content', 'png'),
            ('link', 'href', 'text', ''),
            ('script', 'src', 'text', '')):
        sources = soup.find_all(tag)
        if sources:
            html = download_sources(sources, path_to_files, url, html,
                                    attr, resp_attr, ext)
    return html


def download_sources(sources: List[BeautifulSoup], full_path_to_files: Path,
                     base_url: str, html: str, attr: str, response_attr: str,
                     extension: str = '', ) -> str:
    """Downloads source and put them into full_path_to_files
    Returns changed html"""

    for src in sources:
        src_url = src.get(attr)
        if not src_url and not (
                src_url.startswith('/') or base_url in src_url):
            continue

        base_src_url = src_url
        if src_url.startswith('/'):
            src_url = urljoin(base_url, src_url)

        path_to_src = transform_url_to_file_name(src_url, extension)
        path_to_src = full_path_to_files.joinpath(path_to_src)
        html = html.replace(base_src_url, '/'.join(path_to_src.parts[1:]))

        src_response = get_response(src_url)
        file_txt = src_response.__getattribute__(response_attr)

        write_to_file(path_to_src, file_txt)
    return html
