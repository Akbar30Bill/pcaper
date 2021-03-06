#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Alexander Grechin
#
# Licensed under the BSD 3-Clause license.
# See LICENSE file in the project root for full license information.
#

"""Parse traffic dump in har format
extract HTTP requests including headers and body"""

import argparse
from pcaper import HarParser
from . import _version
import sys


def parse_args():
    """Parse console arguments

    Returns:
        dict: console arguments
    """

    parser = argparse.ArgumentParser(
        description="Parse traffic dump in har format " +
                    "extract HTTP requests including headers and body",
        add_help=True
    )
    parser.add_argument('input', help='har file to parse')
    parser.add_argument('-o', '--output', help='output filename')
    parser.add_argument('-F', '--http-filter', help='HTTP packet filter')
    parser.add_argument(
        '-s', '--stats', help='print stats', action='store_true'
    )
    parser.add_argument(
        '-S', '--stats-only', help='print stats only', action='store_true'
    )
    parser.add_argument(
        '-v', '--version', help='print version', action='version',
        version='{version}'.format(version=_version.__version__)
    )

    return vars(parser.parse_args())


def har2txt(args):
    """Read har file and print HTTP requests

    Args:
        args (dict): console arguments

    Returns:
        int: 0 if Success`, 1 otherwise`
    """

    reader = HarParser()

    if args['output']:
        file_handler = open(args['output'], "w")
    else:
        file_handler = sys.stdout
    try:
        if args['stats_only']:
            for request in reader.read_har(args):
                pass
        else:
            for request in reader.read_har(args):
                file_handler.write("%0.6f: [* -> %s]\n%s\n" % (
                    request.timestamp,
                    request.dst,
                    request.origin
                ))
    except ValueError as e:
        sys.stderr.write('Error: ' + str(e) + "\n")
        return 1

    if file_handler is not sys.stdout:
        file_handler.close()

    if args['stats'] or args['stats_only']:
        print("Stats:")
        stats = reader.get_stats()
        for key in stats.keys():
            print("\t%s: %d" % (key, stats[key]))
    return 0


def main():
    """The main function"""

    args = parse_args()
    return har2txt(args)


def init():
    """Testable init function"""

    if __name__ == '__main__':
        sys.exit(main())


init()
