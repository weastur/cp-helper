#!/usr/bin/env python3

import argparse

from codeforces.parser import parse


class Platform:
    CODEFORCES = 'codeforces'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--platform',
        help='contest platform(only codeforces supported for now)',
        default=Platform.CODEFORCES,
        choices=(
            Platform.CODEFORCES,
        ),
    )
    parser.add_argument(
        '-c',
        '--contest',
        help='contest number',
        type=int,
    )
    args = parser.parse_args()
    if args.platform == Platform.CODEFORCES:
        print(parse(args.contest))


if __name__ == '__main__':
    main()
