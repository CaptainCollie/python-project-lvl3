import re

from urllib.parse import urlparse


def transform_url_to_file_name(url: str, postfix: str,
                               is_dir: bool = False) -> str:
    """Transforms url to file name
    https://ru.hexlet.io/courses -> ru-hexlet-io-courses.html"""
    parsed_url = urlparse(url)
    if len(parsed_url.path.split('.')) == 2:
        if not postfix:
            postfix = parsed_url.path.split('.')[-1]
        parsed_url = parsed_url._replace(
            path=''.join(parsed_url.path.split('.')[:-1]))
    elif not postfix:
        postfix = 'html'
    if not is_dir:
        postfix = '.' + postfix

    if parsed_url.path == '/':
        parsed_url = parsed_url._replace(path='')
    prepared_ulr = re.sub(rf'{parsed_url.scheme}://', '', parsed_url.geturl())
    file_name = re.sub(r'[^\w\d]', '-', prepared_ulr) + postfix
    return file_name
