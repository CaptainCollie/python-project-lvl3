import os

from page_loader.logger import logger_


def create(dir_path):
    try:
        os.mkdir(dir_path)
    except FileExistsError:
        logger_.warning(f'Directory exists: {dir_path}')
