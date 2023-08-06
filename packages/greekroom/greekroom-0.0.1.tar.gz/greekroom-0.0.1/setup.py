#!/usr/bin/env python

import greekroom
from pathlib import Path

from setuptools import setup, find_namespace_packages

long_description = Path('README.md').read_text(encoding='utf-8', errors='ignore')

classifiers = [  # copied from https://pypi.org/classifiers/
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'Topic :: Utilities',
    'Topic :: Text Processing',
    'Topic :: Text Processing :: General',
    'Topic :: Text Processing :: Linguistic',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3 :: Only',
]

setup(
    name='greekroom',
    version=greekroom.__version__,
    description=greekroom.__description__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=classifiers,
    python_requires='>=3.9',
    url='https://github.com/uhermjakob/greekroom',
    download_url='https://github.com/uhermjakob/greekroom',
    platforms=['any'],
    author='Ulf Hermjakob',
    author_email='ulf@isi.edu',
    packages=find_namespace_packages(exclude=['aux']),
    keywords=['machine translation', 'datasets', 'NLP', 'natural language processing,'
                                                        'computational linguistics'],
    entry_points={
        'console_scripts': [
            'greekroom=greekroom.greekroom:main'
        ],
    },
    install_requires=[
        'regex>=2021.8.3',
        'tqdm>=4.40',
    ],
    include_package_data=True,
    zip_safe=False,
)
