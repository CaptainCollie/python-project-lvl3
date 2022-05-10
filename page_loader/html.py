from pathlib import Path
from typing import List
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from progress.bar import ChargingBar

from page_loader.file import write
from page_loader.utils import transform_url_to_file_name, get_response


def replace_links_to_paths(html: str, path_to_files: Path,
                           url: str) -> str:
    parsed_url = urlparse(url)
    base_url = f'{parsed_url.scheme}://{parsed_url.netloc}'
    soup = BeautifulSoup(html, 'html.parser')
    for tag, attr, resp_attr, ext in (
            ('img', 'src', 'content', 'jpg'),
            ('link', 'href', 'text', ''),
            ('script', 'src', 'text', '')):
        sources = soup.find_all(tag)
        if sources:
            html = download_sources(sources, path_to_files, base_url, url,
                                    html, attr, resp_attr, ext)
    return BeautifulSoup(html, 'html.parser').prettify()


def download_sources(sources: List[BeautifulSoup], full_path_to_files: Path,
                     base_url: str, curr_url: str, html: str, attr: str,
                     response_attr: str, extension: str = '', ) -> str:
    """Downloads source and put them into full_path_to_files
    Returns changed html"""

    for src in sources:
        bar = ChargingBar(max=1)
        src_url = src.get(attr)
        parsed_src_url = urlparse(src_url)
        if parsed_src_url.scheme and base_url not in src_url:
            continue

        base_src_url = src_url

        if not parsed_src_url.netloc and parsed_src_url.path.startswith('/'):
            src_url = urljoin(base_url, src_url)
        elif not parsed_src_url.netloc and not parsed_src_url.path.startswith(
                '/'):
            src_url = urljoin(curr_url, src_url)

        bar.message = src_url + ' '
        bar.start()
        path_to_src = transform_url_to_file_name(src_url, extension)
        path_to_src = full_path_to_files.joinpath(path_to_src)
        html = html.replace(base_src_url, '/'.join(path_to_src.parts[3:]))

        src_response = get_response(src_url)
        file_txt = src_response.__getattribute__(response_attr)
        file_txt = to_str(file_txt)

        write(path_to_src, file_txt)
        bar.next()
        bar.finish()

    return html


def to_str(data):
    if isinstance(data, bytes):
        data = data.decode('utf-8', 'ignore')

    data.replace('\xef\xbb\xbf', '')
    return data
