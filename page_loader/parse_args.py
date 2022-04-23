import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(metavar='url', type=str, dest='url')
    parser.add_argument('-o', '--output', dest='output', type=str,
                        metavar='output', help='output dir (default: "/app")',
                        default='/app')

    args = parser.parse_args()
    return args
