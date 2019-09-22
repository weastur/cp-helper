#!/usr/bin/env python3

import argparse

from codeforces.parser import parse
from utils.generators import (
    generate_folder_structure,
    generate_test_files,
    copy_templates,
)


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
        problems = parse(args.contest)
    generate_folder_structure(args.contest, problems)
    generate_test_files(args.contest, problems)
    copy_templates(args.platform, args.contest, problems)


if __name__ == '__main__':
    main()
