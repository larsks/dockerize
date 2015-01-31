import logging
import os
import re
import subprocess
from collections import namedtuple

LOG = logging.getLogger(__name__)
RE_DEPS = [
    re.compile('''\s+ (?P<name>\S+) \s+ => \s+
               (?P<path>\S+) \s+ \((?P<address>0x[0-9a-f]+)\)''',
               re.VERBOSE),
    re.compile('''(?P<path>\S+) \s+ \((?P<address>0x[0-9a-f]+)\)''',
               re.VERBOSE),
    ]

ELFContents = namedtuple('ELFContents',
                         [
                             'index',
                             'name',
                             'size',
                             'vma',
                             'lma',
                             'offset',
                             'aligment',
                         ])


class ELFFile (dict):
    def __init__(self, path):
        self.path = path
        self.read_sections()

    def read_sections(self):
        try:
            out = subprocess.check_output(['objdump', '-h', self.path])
        except subprocess.CalledProcessError:
            raise ValueError(self.path)

        for line in out.splitlines():
            line = line.strip()
            if not line or not line[0].isdigit():
                continue

            contents = ELFContents(*line.split())
            self[contents.name] = contents

    def section(self, name):
        section = self[name]
        with open(self.path) as fd:
            fd.seek(int(section.offset, base=16))
            data = fd.read(int(section.size, base=16))
            return data

    def interpreter(self):
        return self.section('.interp').rstrip('\0')


class DepSolver (object):
    '''Finds library dependencies of ELF binaries.'''

    def __init__(self, arch=None):
        self.deps = set()

    def get_deps(self, path):
        LOG.info('getting dependencies for %s', path)

        try:
            ef = ELFFile(path)
            interp = ef.interpreter()
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

        # skip the first line of output, which will be the
        # binary itself.
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
        self.get_deps(path)

    def prefixes(self):
        return set(os.path.dirname(path) for path in self.deps)
