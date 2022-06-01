import argparse

from page_loader.scripts import logger_


def parse_args():
    parser = argparse.ArgumentParser(
        add_help=False,
        usage="Usage page-loader [options] <url>",
        description="some description",
    )
    parser.add_argument(metavar='url', type=str, dest='url')
    parser.add_argument('-V', '--version', help='output the version number',
                        action='version', version='0.1.0')
    parser.add_argument('-o', '--output', dest='output', type=str,
                        metavar='output', help='output dir (default: "/app")',
                        default='/app')
    parser._optionals.title = 'Options'
    args = parser.parse_args()
    logger_.info(f'Args: {args}')
    return args
