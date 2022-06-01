#! usr/env/python

from page_loader.html import download
from page_loader.parse_args import parse_args
from page_loader.scripts import logger_


def main():
    try:
        args = parse_args()
        file_path = download(args.url, args.output)
        print(f"Page was successfully downloaded into '{file_path}'")
    except (FileExistsError, PermissionError) as e:
        logger_.error(str(e))


if __name__ == "__main__":
    main()
