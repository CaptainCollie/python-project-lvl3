import requests

from page_loader.logger import logger_


def make_request(url):
    logger_.info(f'Request to {url}')
    response = requests.get(url)
    logger_.info(f'Response status {response.status_code}')
    response.raise_for_status()
    return response
