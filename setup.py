#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst
# -*- encoding: utf-8 -*-

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext
from setuptools import setup, find_packages


def readme():
    with open('README.rst') as ff:
        return ff.read()


setup(
    name='pytest-remotedata',
    version='0.3.1',
    license='BSD',
    description='Pytest plugin for controlling remote data access.',
    long_description=readme(),
    author='The Astropy Developers',
    author_email='astropy.team@gmail.com',
    url='https://astropy.org',
    packages=find_packages(exclude=['tests']),
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ],
    keywords=[ 'remote', 'data', 'pytest', 'py.test' ],
    install_requires=[ 'six', 'pytest>=3.1' ],
    python_requires='>=2.7',
    entry_points={
        'pytest11': [
            'pytest_remotedata = pytest_remotedata.plugin',
        ],
    },
)
