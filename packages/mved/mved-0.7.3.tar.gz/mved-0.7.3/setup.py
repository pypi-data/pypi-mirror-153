#!/usr/bin/env python
# This file is part of mved, the bulk file renaming tool.
# License: GNU GPL version 3, see the file "AUTHORS" for details.

from setuptools import setup, find_packages
import runpy


version = runpy.run_path('mved/_version.py')['__version__']

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="mved",
    version=version,
    description="Bulk-rename, copy and delete files using a text editor",
    long_description=long_description,
    author="Daniel K.",
    author_email="code@ferreum.de",
    url="https://gitlab.com/ferreum/mved",
    packages=find_packages('.', exclude=['tests', 'tests.*']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Desktop Environment :: File Managers',
        'Topic :: Utilities',
    ],
    install_requires=[
        'simplediff>=1.1,<2.0',
    ],
    entry_points={
        'console_scripts': [
            'mved = mved:main',
        ]
    },
    data_files=[
        ('share/vim/vimfiles/syntax', ['etc/vim/syntax/mved.vim']),
        ('share/vim/vimfiles/ftdetect', ['etc/vim/ftdetect/mved.vim']),
    ],
)
