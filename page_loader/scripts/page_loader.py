#! usr/env/python
import requests

from pathlib import Path
from page_loader.parse_args import parse_args
from page_loader.utils import transform_url_to_file_name


def download(url, path):
    path_to_dir = Path(path)
    if not path_to_dir.exists():
        raise ValueError(f'Path {path} do not exist')

    response = requests.get(url)
    if not response.status_code == 200:
        raise ConnectionError(f'Connection to {url} failed')

    path_to_file = transform_url_to_file_name(url)
    full_path = path_to_dir.joinpath(path_to_file).absolute()
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(response.text)
    return full_path


def main():
    args = parse_args()
    file_path = download(args.url, args.output)
    print(file_path)


if __name__ == "__main__":
    main()