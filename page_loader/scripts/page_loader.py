#! usr/env/python

from page_loader.html import download
from page_loader.parse_args import parse_args


def main():
    args = parse_args()
    file_path = download(args.url, args.output)
    print(f"Page was successfully downloaded into '{file_path}'")


if __name__ == "__main__":
    main()
