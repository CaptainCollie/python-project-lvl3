from pathlib import Path
from typing import Union

from page_loader.logger import logger_


def write(path: Union[Path, str], data: Union[str, bytes]) -> None:
    data = to_bytes(data)
    logger_.info(f'Writing in file {path}')
    with open(path, 'wb') as f:
        f.write(data)


def to_bytes(text):
    if isinstance(text, str):
        text = text.encode('utf-8-sig', 'ignore')
    return text
