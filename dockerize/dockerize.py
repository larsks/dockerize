import glob
import grp
import json
import logging
import os
import pwd
import shlex
import shutil
import subprocess
import tempfile
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

        self.docker = {}
        if cmd:
            self.docker['cmd'] = json.dumps(shlex.split(cmd))
        if entrypoint:
            self.docker['entrypoint'] = json.dumps(shlex.split(entrypoint))
        if tag:
            self.docker['tag'] = tag

        self._targetdir = targetdir
        self._build_image = build

        self.users = []
        self.groups = []
        self.paths = set()
        self.env = Environment(loader=PackageLoader('dockerize', 'templates'))

    def add_user(self, user):
        LOG.info('adding user %s', user)
        if ':' in user:
            self.users.append(user)
        else:
            pwent = pwd.getpwnam(user)
            self.users.append(':'.join(str(x) for x in pwent))
            grent = grp.getgrgid(pwent.pw_gid)
            self.groups.append(':'.join(str(x) for x in
                                        grent[:3] + (','.join(grent[3]),)
                                        if not isinstance(x, list)))

    def add_group(self, group):
        LOG.info('adding group %s', group)
        if ':' in group:
            self.groups.append(group)
        else:
            grent = grp.getgrnam(group)
            self.groups.append(':'.join(str(x) for x in grent))

    def add_file(self, src, dst=None, static=False):
        if dst is None:
            dst=src

        if not dst.startswith('/'):
            raise ValueError('%s: container paths must be fully '
                             'qualified' % dst)

        self.paths.add((src, dst, static))

    def build(self):
        LOG.info('start build process')
        cleanup=False
        try:
            if not self._targetdir:
                self._targetdir = tempfile.mkdtemp(prefix='dockerize')
                cleanup=True
            else:
                if not os.path.isdir(self._targetdir):
                    os.mkdir(self._targetdir)

            self.copy_files()
            self.resolve_deps()
            self.populate()
            self.generate_dockerfile()
            if self._build_image:
                self.build_image()
        finally:
            if cleanup:
                shutil.rmtree(self._targetdir,
                              ignore_errors=True)

    def generate_dockerfile(self):
        LOG.info('generating Dockerfile')
        tmpl = self.env.get_template('Dockerfile')
        with open(os.path.join(self._targetdir, 'Dockerfile'), 'w') as fd:
            fd.write(tmpl.render(controller=self,
                                 docker=self.docker))

    def makedirs(self, path):
        if not os.path.isdir(path):
            os.makedirs(path)

    def populate(self):
        LOG.info('populating misc config files')
        self.makedirs(os.path.join(self._targetdir, 'etc'))
        for path in ['passwd', 'group', 'nsswitch.conf']:
            tmpl = self.env.get_template(path)
            with open(os.path.join(self._targetdir, 'etc', path), 'w') as fd:
                fd.write(tmpl.render(controller=self,
                                     docker=self.docker,
                                     users=self.users,
                                     groups=self.groups))

    def copy_file(self, src, dst=None):
        if dst is None:
            dst = src

        LOG.info('copying file %s to %s', src, dst)
        target = os.path.join(self._targetdir, dst[1:])
        target_dir = os.path.dirname(target)
        self.makedirs(target_dir)

        if os.path.isdir(src):
            shutil.copytree(src, target, symlinks=True)
        else:
            shutil.copy(src, target)

    def resolve_deps(self):
        deps = DepSolver()

        for root, dirs, files in os.walk(self._targetdir):
            for name in files:
                path = os.path.join(root, name)
                deps.add(path)

        for src in deps.deps:
            self.copy_file(src)

        for interp in deps.interps:
            libdir = os.path.dirname(interp)
            for nsslib in ['libnss_dns.so.2',
                           'libnss_files.so.2',
                           'libnss_compat.so.2']:
                src = os.path.join(libdir, nsslib)
                if os.path.exists(src):
                    self.copy_file(src)

    def copy_files(self):
        for src, dst, static in self.paths:
            for srcitem in glob.iglob(src):
                self.copy_file(srcitem, dst)

    def build_image(self):
        LOG.info('building Docker image')
        cmd = ['docker', 'build']
        if self.docker.get('tag'):
            cmd += ['-t', self.docker['tag']]

        cmd += [self._targetdir]

        subprocess.check_call(cmd)
