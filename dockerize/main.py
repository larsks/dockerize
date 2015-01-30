#!/usr/bin/python

import argparse
import logging
import glob
import os

from dockerize import Dockerize

LOG = logging.getLogger('dockerize')


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--tag', '-t')
    p.add_argument('--cmd', '-c')
    p.add_argument('--target-dir', '-o')
    p.add_argument('--no-build', '-n',
                   action='store_true')
    p.add_argument('--entrypoint', '-e')
    p.add_argument('--add-file', '-a',
                   action='append',
                   default=[])
    p.add_argument('paths', nargs='*')

    return p.parse_args()

if __name__ == '__main__':
    args = parse_args()
    logging.basicConfig(level=logging.DEBUG)
    if args.entrypoint is None and args.cmd is None:
        args.entrypoint = args.paths[0]

    app = Dockerize(cmd=args.cmd,
                    entrypoint=args.entrypoint,
                    tag=args.tag,
                    targetdir=args.target_dir,
                    build=not args.no_build)

    for path in args.paths:
        app.add_binary(path)

    for path in args.add_file:
        for expanded in glob.iglob(path):
            app.add_file(expanded)

    app.build()
