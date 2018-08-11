#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# OpenStack Monitoring
# Copyright (C) 2015 Tobias Urdin

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import os

from distutils.core import setup
from distutils.core import Command
from unittest import TextTestRunner, TestLoader
from subprocess import call


class TestCommand(Command):
    description = "run test"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        status = self._run_tests()
        sys.exit(status)

    def _run_tests(self):
        print "hello world"


class Pep8Command(Command):
    description = "run pep8"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        status = self._run_tests()
        sys.exit(status)

    def _run_tests(self):
        try:
            import pep8
            pep8
        except ImportError:
            print('Missing "pep8" library. You can install it using pip:'
                  'pip install pep8')
            sys.exit(1)

        cwd = os.getcwd()
        retcode = call(('pep8 %s/openstack_monitoring/ %s/test/' %
                        (cwd, cwd)).split(' '))

        sys.exit(retcode)


class CoverageCommand(Command):
    description = "run coverage"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
           import coverage
        except ImportError:
            print('Missing "coverage" library. You can install it using pip:'
                  'pip install coverage')
            sys.exit(1)

        cover = coverage.coverage(config_file='.coveragerc')
        cover.start()

        tc = TestCommand(self.distribution)
        tc._run_tests()

        cover.stop()
        cover.save()
        cover.html_report()

setup(name='openstack-monitoring',
      version='1.0',
      description='OpenStack Monitoring checks for Nagios and its forks.',
      author='Tobias Urdin',
      author_email='tobias.urdin@gmail.com',
      license='Apache License 2.0',
      packages=['openstack_monitoring'],
      package_dir={
          'openstack_monitoring': 'openstack_monitoring',
      },
      url='https://github.com/tobias-urdin/openstack-monitoring',
      cmdclass={
          'test': TestCommand,
          'pep8': Pep8Command,
          'coverage': CoverageCommand
      },
      )
