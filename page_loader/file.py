from pathlib import Path
from typing import Union

from page_loader.logger import logger_


def write(path: Union[Path, str], data: Union[str, bytes]) -> None:
    logger_.info(f'Writing in file {path}')
    with open(path, 'w') as f:
        f.write(data)
