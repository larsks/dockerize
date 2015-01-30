import subprocess
import logging
import re
from elftools.elf.elffile import ELFFile

LOG = logging.getLogger(__name__)
re_dep = re.compile(r'''\s+ (?P<name>\S+) \s+ => (\s+ (?P<path>/\S+))?
                    \s+ \((?P<hash>[^)]+)\)''', re.VERBOSE)


class DepSolver (object):
    def __init__(self, arch=None):
        self.deps = set()
        self.interps = set()

    def get_interp(self, path):
        LOG.info('getting interpreter for %s', path)
        with open(path) as fd:
            ef = ELFFile(fd)
            s = ef.get_section_by_name('.interp')
            if not s:
                return

            interp = s.data().rstrip('\0')
            self.deps.add(interp)
            self.interps.add(interp)
            LOG.info('found interpreter %s for path %s',
                     interp,
                     path)

    def get_deps(self, path):
        LOG.info('getting dependencies for %s', path)
        p = subprocess.Popen(['ldd', path],
                             stdout=subprocess.PIPE)
        out, err = p.communicate()

        for line in out.splitlines():
            match = re_dep.match(line)
            if match and match.group('path'):
                LOG.debug('%s requires %s',
                          path,
                          match.group('path'))
                if not match.group('path') in self.deps:
                    self.get_deps(match.group('path'))
                self.deps.add(match.group('path'))

    def add(self, path):
        self.get_interp(path)
        self.get_deps(path)
