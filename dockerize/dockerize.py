import os
import shutil
import shlex
import tempfile
import json
import subprocess
import logging
from jinja2 import Environment, PackageLoader
from depsolver import DepSolver

LOG = logging.getLogger(__name__)


class Dockerize (object):
    def __init__(self,
                 cmd=None,
                 entrypoint=None,
                 targetdir=None,
                 tag=None,
                 build=True):

        self.cmd = cmd
        self.entrypoint = entrypoint
        self.targetdir = targetdir
        self._do_build_image = build

        if self.cmd:
            self.cmd = json.dumps(shlex.split(cmd))

        if self.entrypoint:
            self.entrypoint = json.dumps(shlex.split(entrypoint))

        self.tag = tag
        self.paths = set()
        self.deps = DepSolver()
        self.env = Environment(loader=PackageLoader('dockerize', 'templates'))

    def add_file(self, path):
        LOG.info('adding %s', path)
        self.paths.add(path)

    def add_binary(self, path):
        self.add_file(path)
        self.deps.add(path)

    def build(self):
        LOG.info('start build process')
        try:
            if not self.targetdir:
                self.targetdir = tempfile.mkdtemp(prefix='dockerize')
                cleanup=True
            else:
                os.mkdir(self.targetdir)
                cleanup=False

            self.copy_files()
            self.populate()
            self.generate_dockerfile()
            if self._do_build_image:
                self.build_image()
        finally:
            if cleanup:
                shutil.rmtree(self.targetdir,
                              ignore_errors=True)

    def generate_dockerfile(self):
        LOG.info('generating Dockerfile')
        tmpl = self.env.get_template('Dockerfile')
        with open(os.path.join(self.targetdir, 'Dockerfile'), 'w') as fd:
            fd.write(tmpl.render(model=self))

    def makedirs(self, path):
        if not os.path.isdir(path):
            os.makedirs(path)

    def populate(self):
        LOG.info('populating misc config files')
        self.makedirs(os.path.join(self.targetdir, 'etc'))
        for path in ['passwd', 'group', 'nsswitch.conf']:
            tmpl = self.env.get_template(path)
            with open(os.path.join(self.targetdir, 'etc', path), 'w') as fd:
                fd.write(tmpl.render(model=self))

        for interp in self.deps.interps:
            libdir = os.path.dirname(interp)
            for nsslib in ['libnss_dns.so.2',
                           'libnss_files.so.2',
                           'libnss_compat.so.2']:
                src = os.path.join(libdir, nsslib)
                if os.path.exists(src):
                    self.copy_file(src)

    def copy_file(self, path):
        LOG.info('copying file %s', path)
        target = os.path.join(self.targetdir, path[1:])
        target_dir = os.path.dirname(target)
        self.makedirs(target_dir)
        shutil.copy(path, target)

    def copy_files(self):
        for path in self.paths.union(self.deps.deps):
            if os.path.isdir(path):
                self.copy_dir(path)
            else:
                self.copy_file(path)

    def copy_dir(self, path):
        LOG.info('copying directory %s', path)
        target = os.path.join(self.targetdir, path[1:])
        target_dir = os.path.dirname(target)
        shutil.copytree(path, target)

    def build_image(self):
        LOG.info('building Docker image')
        cmd = ['docker', 'build']
        if self.tag:
            cmd += ['-t', self.tag]

        cmd += [self.targetdir]

        subprocess.check_call(cmd)
