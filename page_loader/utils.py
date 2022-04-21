import re
from urllib.parse import urlparse


def transform_url_to_file_name(url):
    parsed_url = urlparse(url)
    if len(parsed_url.path.split('.')) == 2:
        parsed_url = parsed_url._replace(
            path=''.join(parsed_url.path.split('.')[:-1]))
    prepared_ulr = re.sub(rf'{parsed_url.scheme}://', '', parsed_url.geturl())
    file_name = re.sub(r'[^\w\d]', '-', prepared_ulr) + '.html'
    return file_name
