from pathlib import Path
from typing import List
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from progress.bar import ChargingBar

from page_loader.file import write
from page_loader.request import make_request
from page_loader.url import transform_url_to_path


#  Не получилось разбить эту функцию
def update_html(html: str, path_to_files: Path, url: str) -> str:
    data_for_downloading = parse_html(html)
    for sources, attr, ext, resp_attr in data_for_downloading:
        sources_to_download = get_sources_to_download(sources,
                                                      attr,
                                                      ext,
                                                      path_to_files,
                                                      url)

        for url, path, url_to_replace in sources_to_download:
            bar = ChargingBar(max=1)
            bar.message = url + ' '
            bar.start()

            download_source(url, path, resp_attr)
            html = html.replace(url_to_replace, ''.join(path.parts[3:]))

            bar.next()
            bar.finish()
    return BeautifulSoup(html, 'html.parser').prettify()


def parse_html(html: str) -> list:
    soup = BeautifulSoup(html, 'html.parser')
    data_for_downloading = (('img', 'src', 'content', 'jpg'),
                            ('link', 'href', 'content', ''),
                            ('script', 'src', 'text', ''))

    result = []
    for tag, attr, resp_attr, ext in data_for_downloading:
        sources = soup.find_all(tag)
        result.append((sources, attr, ext, resp_attr))
    return result


def get_sources_to_download(sources: List[BeautifulSoup],
                            attr: str,
                            extension: str,
                            full_path_to_files: Path,
                            url: str, ):
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

        path_to_src = transform_url_to_path(src_url, extension)
        path_to_src = full_path_to_files.joinpath(path_to_src)

        sources_to_download.append((src_url, path_to_src, base_src_url))

    return sources_to_download


def download_source(src_url: str, path_to_src: Path, response_attr: str, ):
    src_response = make_request(src_url)
    file_txt = src_response.__getattribute__(response_attr)

    write(path_to_src, file_txt)
