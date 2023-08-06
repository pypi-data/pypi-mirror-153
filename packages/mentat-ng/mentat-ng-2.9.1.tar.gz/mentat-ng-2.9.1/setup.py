#!/usr/bin/python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Author: Jan Mach <jan.mach@cesnet.cz>
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Usage
--------------------------------------------------------------------------------

Install package locally for development:

    pip install -e .[dev]

Resources:
--------------------------------------------------------------------------------

* https://packaging.python.org/en/latest/
* https://python-packaging.readthedocs.io/en/latest/index.html
* https://setuptools.readthedocs.io/en/latest/setuptools.html

"""


import sys
import os

# To use a consistent encoding
from codecs import open
# Always prefer setuptools over distutils
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

sys.path.insert(0, os.path.abspath('lib'))
import mentat

#-------------------------------------------------------------------------------

def read_file(file_name):
    """Read file and return its contents."""
    with open(file_name, 'r') as fhd:
        return fhd.read()

def read_requirements(file_name):
    """Read requirements file as a list."""
    reqs = read_file(file_name).splitlines()
    if not reqs:
        raise RuntimeError(
            "Unable to read requirements from the {} file.".format(
                file_name
            )
        )
    reqs = [req.split(' ')[0] for req in reqs]
    return reqs

#-------------------------------------------------------------------------------

# Get the long description from the README file
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as fhnd:
    long_description = fhnd.read()

setup(
    name = 'mentat-ng',
    version = mentat.__version__,
    description = 'Distributed modular SIEM system designed to monitor networks of all sizes',
    long_description = long_description,
    classifiers = [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only'
    ],
    keywords = 'library',
    url = 'https://homeproj.cesnet.cz/git/mentat-ng.git',
    author = 'CESNET-CERTS Development Team',
    author_email = 'csirt@cesnet.cz',
    license = 'MIT',
    package_dir = {'': 'lib'},
    packages = find_packages('lib'),
    test_suite = 'nose.collector',
    tests_require = [
        'nose'
    ],
    install_requires = read_requirements('conf/requirements.pip'),
    # Add development requirements as extras. This way it is possible to install
    # the package for development locally with following command:
    #
    #   pip install -e .[dev]
    #
    # Resources:
    #   https://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-extras-optional-features-with-their-own-dependencies
    #   https://stackoverflow.com/a/28842733
    extras_require = {
        'dev': read_requirements('conf/requirements-dev.pip'),
    },
    scripts = [
        'bin/mentat-backup.py',
        'bin/mentat-cleanup.py',
        'bin/mentat-controller.py',
        'bin/mentat-dbmngr.py',
        'bin/mentat-enricher.py',
        'bin/mentat-hawat.wsgi',
        'bin/mentat-hawat-dev.wsgi',
        'bin/mentat-ideagen.py',
        'bin/mentat-informant.py',
        'bin/mentat-inspector.py',
        'bin/mentat-netmngr.py',
        'bin/mentat-precache.py',
        'bin/mentat-reporter.py',
        'bin/mentat-sampler.py',
        'bin/mentat-statistician.py',
        'bin/mentat-storage.py'
    ],
    # Add entry point to custom command line interface.
    #
    # Resources:
    #   http://flask.pocoo.org/docs/1.0/cli/#custom-commands
    entry_points={
        'console_scripts': [
            'hawat-cli=hawat:cli'
        ],
    },
    include_package_data = True,
    zip_safe = False
)
