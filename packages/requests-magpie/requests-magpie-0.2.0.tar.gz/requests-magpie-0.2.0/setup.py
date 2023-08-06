#!/usr/bin/env python
# coding: utf-8
import os
import re
from setuptools import setup

path = os.path.dirname(__file__)
desc_fd = os.path.join(path, 'README.rst')
hist_fd = os.path.join(path, 'HISTORY.rst')

long_desc = ''
short_desc = 'A Magpie authentication handler for python-requests'

if os.path.isfile(desc_fd):
    with open(desc_fd) as fd:
        long_desc = fd.read()

if os.path.isfile(hist_fd):
    with open(hist_fd) as fd:
        long_desc = '\n\n'.join([long_desc, fd.read()])


def get_version():
    """
    Simple function to extract the current version using regular expressions.
    """
    reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
    with open('requests_magpie.py') as fd:
        matches = list(filter(lambda x: x, map(reg.match, fd)))

    if not matches:
        raise RuntimeError(
            'Could not find the version information for requests_magpie'
            )

    return matches[0].group(1)


setup(
    name='requests-magpie',
    description=short_desc,
    long_description=long_desc,
    author='David Caron',
    author_email='david.caron@crim.ca',
    url='https://github.com/ouranosinc/requests-magpie',
    py_modules=['requests_magpie'],
    license='ISC',
    version=get_version(),
    install_requires=[
        'requests>=1.1.0',
    ],
    extras_require={
    },
    tests_require=['mock'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
