#! usr/env/python
from pathlib import Path
from typing import Union, Optional

from page_loader.loader import download_
from page_loader.parse_args import parse_args

__all__ = ['download']


def download(url: str, path: Union[str, Path]) -> Optional[str]:
    """Download html page located on url and save it to path/url.html"""
    return download_(url, path)


def main():
    args = parse_args()
    file_path = download(args.url, args.output)
    print(f"Page was successfully downloaded into '{file_path}'")


if __name__ == "__main__":
    main()
