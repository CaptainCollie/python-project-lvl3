import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(metavar='url', type=str, dest='url')
    parser.add_argument('-o', '--output-file', dest='output', type=str,
                        metavar='output',
                        help='Path to save downloaded page', default='')
    args = parser.parse_args()
    return args
