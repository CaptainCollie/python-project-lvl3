from pathlib import Path
from typing import Union

from page_loader.logger import logger_


def choose_mode(file_txt: Union[str, bytes]) -> str:
    if isinstance(file_txt, bytes):
        return 'wb'
    elif isinstance(file_txt, str):
        return 'w'
    return ''


def write(path: Union[Path, str], data: Union[str, bytes]) -> None:
    mode = choose_mode(data)
    logger_.info(f'Writing in file {path}')
    encoding_dict = {'encoding': 'utf-8'} if mode == 'w' else {}
    with open(path, mode, **encoding_dict) as f:
        f.write(data)
