import re
from urllib.parse import urlparse


def transform_to_path(url: str, extension: str = '',
                      is_dir: bool = False) -> str:
    """Transforms url to file name
    https://ru.hexlet.io/courses -> ru-hexlet-io-courses.html"""
    parsed_url = urlparse(url)
    file_raw_extension = re.search(r'\.\w+$', parsed_url.path)
    if file_raw_extension:
        file_raw_extension = file_raw_extension.group()
        url = url.replace(file_raw_extension, '')
    elif not extension:
        extension = '.html'
    if not extension:
        extension = file_raw_extension

    prepared_ulr = url.replace(f'{parsed_url.scheme}://', '')
    file_name = re.sub(r'[^\w\d]', '-',
                       prepared_ulr) + ('_files' if is_dir else extension)
    return file_name
