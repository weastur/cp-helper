#!/usr/bin/env python3

import argparse


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


if __name__ == '__main__':
    main()
