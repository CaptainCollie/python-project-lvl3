import requests

from page_loader.logger import logger_


def make_request(url):
    logger_.info(f'Request to {url}')
    response = requests.get(url)
    logger_.info(f'Response status {response.status_code}')
    if response.status_code != 200:
        logger_.error(f'Connection to {url} failed\n'
                      f'{response.status_code}')
        raise ConnectionError(f'Connection to {url} failed\n'
                              f'{response.reason}\n'
                              f'{response.status_code}'
                              )
    return response
