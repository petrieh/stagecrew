import os
import random
import string
import shutil
import pytest

from .runner import Runner
from .verifier import EndToEndVerifier

THISDIR = os.path.dirname(__file__)
EXAMPLE_PACKAGE_DIR = os.path.join(THISDIR, 'examples')


@pytest.fixture(params=[EndToEndVerifier])
def importer_verify(request, package, runner):
    def verify(importer):
        request.param(package=package,
                      runner=runner).verify(importer)

    return verify


@pytest.fixture(name='runner')
def fixture_runner():
    try:
        p = Runner()
        p.start()
        yield p
    finally:
        p.task_queue.put('')
        try:
            p.close()
        except ValueError:
            p.kill()


@pytest.fixture(name='package', params=[EXAMPLE_PACKAGE_DIR])
def fixture_package(request, tmpdir):
    return Package(source_path=request.param, tmpdir=tmpdir)


class Package(object):
    def __init__(self, source_path, tmpdir):
        self._source_path = source_path
        self._tmpdir = tmpdir
        self._name = ''.join(random.choice(string.ascii_letters) for _ in range(10))
        self._initialize()

    def _initialize(self):
        package_path = os.path.join(str(self._tmpdir), self._name)
        shutil.copytree(self._source_path, package_path)

    @property
    def tmpdir(self):
        return self._tmpdir

    @property
    def name(self):
        return self._name
