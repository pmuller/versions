#!/usr/bin/env python

import os
from setuptools import setup, find_packages

import versions


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='versions',
    version=versions.__version__,
    description='Package version handling library',
    long_description=read('README.rst'),
    author='Philippe Muller',
    url='http://github.com/pmuller/versions',
    license='MIT',
    packages=find_packages(),
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Software Distribution',
    ),
    test_suite='nose.collector',
    tests_require=['nose'],
)
