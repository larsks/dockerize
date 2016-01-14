#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import re
import subprocess
from collections import namedtuple

LOG = logging.getLogger(__name__)

RE_DEPS = [
    re.compile(r'''\s+ (?P<name>\S+) \s+ => \s+
               (?P<path>\S+) \s+ \((?P<address>0x[0-9a-f]+)\)''',
               re.VERBOSE),
    re.compile(r'''(?P<path>\S+) \s+ \((?P<address>0x[0-9a-f]+)\)''',
               re.VERBOSE)
    ]

ELFContents = namedtuple('ELFContents',
                         [
                             'index',
                             'name',
                             'size',
                             'vma',
                             'lma',
                             'offset',
                             'aligment'
                         ])


class ELFFile(dict):

    def __init__(self, path):
        self.path = path
        self.read_sections()

    def read_sections(self):
        '''Use `objdump` to read list of sections from the ELF file.'''
        try:
            out = subprocess.check_output(['objdump', '-h', self.path],
                                          stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            raise ValueError(self.path)

        for line in out.splitlines():
            line = line.strip()
            if not line or not line[0].isdigit():
                continue

            contents = ELFContents(*line.split())
            self[contents.name] = contents

    def section(self, name):
        '''Return the raw content of the named section from the ELF file.'''
        section = self[name]
        with open(self.path) as fde:
            fde.seek(int(section.offset, base=16))
            data = fde.read(int(section.size, base=16))
            return data

    def interpreter(self):
        '''Return the value of the `.interp` section of the ELF file.'''
        return self.section('.interp').rstrip('\0')


class DepSolver(object):

    '''Finds shared library dependencies of ELF binaries.'''

    def __init__(self):
        self.deps = set()

    def get_deps(self, path):
        LOG.info('getting dependencies for %s', path)

        # Get the path to the dynamic loader from the ELF .interp
        # section.  We need this because we use the dynamic loader
        # to produce the list of library dependencies.
        try:
            elf = ELFFile(path)
            interp = elf.interpreter()
        except ValueError:
            LOG.debug('%s is not a dynamically linked ELF binary (ignoring)',
                      path)
            return
        except KeyError:
            LOG.debug('%s does not have a .interp section',
                      path)
            return

        self.deps.add(interp)
        out = subprocess.check_output([interp, '--list', path])

        for line in out.splitlines():
            for exp in RE_DEPS:
                match = exp.match(line)
                if not match:
                    continue

                dep = match.group('path')
                LOG.debug('%s requires %s',
                          path,
                          dep)

                self.deps.add(dep)

    def add(self, path):
        '''Add dependencies in `path` to dependencies in self.deps.'''
        self.get_deps(path)

    def prefixes(self):
        '''Return a set of directory prefixes for dependencies.  This is
        useful if you need to know where to look for other libraries.'''

        return set(os.path.dirname(path) for path in self.deps)
