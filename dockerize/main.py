#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import argparse
import logging
import sys

from . import __description__, __program__, __version__
from .dockerize import Dockerize, SymlinkOptions

LOG = logging.getLogger(__name__)

FILETOOLS = [
    '/bin/ls',
    '/bin/mkdir',
    '/bin/chmod',
    '/bin/chown',
    '/bin/rm',
    '/bin/cat',
    '/bin/grep',
    '/bin/sed',
]


def parse_args():
    parser = argparse.ArgumentParser(description=__description__)

    group = parser.add_argument_group('Docker options')
    group.add_argument('--tag', '-t',
                       help='Tag to apply to Docker image')
    group.add_argument('--cmd', '-c')
    group.add_argument('--entrypoint', '-e')

    group = parser.add_argument_group('Output options')
    group.add_argument('--no-build', '-n',
                       action='store_true',
                       help='Do not build Docker image')
    group.add_argument('--output-dir', '-o')

    parser.add_argument('--add-file', '-a',
                        metavar=('SRC', 'DST'),
                        nargs=2,
                        action='append',
                        default=[],
                        help='Add file <src> to image at <dst>')

    parser.add_argument('--symlinks', '-L',
                        default='copy-unsafe',
                        help='One of preserve, copy-unsafe, '
                        'skip-unsafe, copy-all')
    parser.add_argument('--user', '-u',
                        action='append',
                        default=[],
                        help='Add user to /etc/passwd in image')
    parser.add_argument('--group', '-g',
                        action='append',
                        default=[],
                        help='Add group to /etc/group in image')

    parser.add_argument('--filetools',
                        action='store_true',
                        help='Add common file manipulation tools')

    group = parser.add_argument_group('Logging options')
    group.add_argument('--verbose',
                       action='store_const',
                       const=logging.INFO,
                       dest='loglevel')
    group.add_argument('--debug',
                       action='store_const',
                       const=logging.DEBUG,
                       dest='loglevel')

    parser.add_argument('--version',
                        action='version',
                        version='%s version %s' % (__program__, __version__))
    parser.add_argument('paths', nargs=argparse.REMAINDER)
    parser.set_defaults(loglevel=logging.WARN)

    return parser.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level=args.loglevel)

    try:
        args.symlinks = getattr(SymlinkOptions,
                                args.symlinks.upper().replace('-', '_'))
    except AttributeError:
        LOG.error('%s: invalid symlink mode', args.symlinks)
        sys.exit(1)

    # If there is a single binary specified on the command line
    # and there is not an explicit entrypoint, configure
    # that binary as the entrypoint.
    if len(args.paths) == 1 and not args.entrypoint:
        args.entrypoint = args.paths[0]

    app = Dockerize(cmd=args.cmd,
                    entrypoint=args.entrypoint,
                    tag=args.tag,
                    targetdir=args.output_dir,
                    build=not args.no_build,
                    symlinks=args.symlinks)

    for path in args.paths:
        app.add_file(path)

    for src, dst in args.add_file:
        app.add_file(src, dst)

    if args.filetools:
        for path in FILETOOLS:
            app.add_file(path)

    for user in args.user:
        app.add_user(user)

    for group in args.group:
        app.add_group(group)

    app.build()


if __name__ == '__main__':
    main()
