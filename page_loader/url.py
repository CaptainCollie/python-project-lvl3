import re
from urllib.parse import urlparse


def transform_url_to_path(url: str, extension: str = '',
                          is_dir: bool = False) -> str:
    """Transforms url to file name
    https://ru.hexlet.io/courses -> ru-hexlet-io-courses.html"""
    parsed_url = urlparse(url)
    file_raw_extension = ''
    if len(parsed_url.path.split('.')) == 2:
        file_raw_extension = parsed_url.path.split('.')[-1]
        parsed_url = parsed_url._replace(
            path=''.join(parsed_url.path.split('.')[:-1]))

    if not extension and not file_raw_extension:
        extension = 'html'
    elif not extension:
        extension = file_raw_extension

    if not is_dir:
        extension = '.' + extension

    if parsed_url.path == '/':
        parsed_url = parsed_url._replace(path='')
    prepared_ulr = parsed_url.geturl().replace(f'{parsed_url.scheme}://', '')
    file_name = re.sub(r'[^\w\d]', '-', prepared_ulr) + extension
    return file_name
