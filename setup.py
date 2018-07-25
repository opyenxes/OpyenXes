#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from os.path import splitext, basename
from glob import glob


__author__ = 'Wai Lam Jonathan Lee'
__email__ = 'walee@uc.cl'


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    # TODO: put package requirements here
]

setup_requirements = [
    'pytest-runner',
    # TODO(wailamjonathanlee): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # TODO: put package test requirements here
]

setup(
    name='opyenxes',
    version='0.3.0',
    description="A python implementation of the XES standard based on the Java implementation OpenXes.",
    long_description=readme + '\n\n' + history,
    author="Process Mining UC",
    author_email='processmininguc@gmail.com',
    url='https://github.com/opyenxes/OpyenXes',
    entry_points={
        'console_scripts': ['opyenxes=opyenxes.cli:main'],
        'pytest11': ['opyenxes = opyenxes']
    },
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords=['opyenxes', 'xes', 'process mining'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')]
)
