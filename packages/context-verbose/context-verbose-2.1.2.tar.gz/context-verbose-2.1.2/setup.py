#!/usr/bin/env python3

"""
** Configuration file for pypi. **
----------------------------------

#!/bin/bash

python3 setup.py check -s -r
python3 -m pip install --user --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel
python3 -m pip install --user --upgrade twine
python3 -m twine upload --repository pypi dist/*
twine check dist/*
"""

import setuptools

import context_verbose

with open('README.rst', 'r', encoding='utf-8') as file:
    long_description = file.read()

setuptools.setup(
    name='context-verbose',
    version=context_verbose.__version__,
    author='Robin RICHARD (robinechuca)',
    author_email='raisin@ecomail.fr',
    description='Tool to simply display information about the state of the code during its execution.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://framagit.org/robinechuca/context-verbose/-/blob/main/README.rst',
    packages=setuptools.find_packages(),
    install_requires=['colorama', 'networkx'],
    extras_require={
        'tests': ['pytest'],
        'documentation': ['pdoc3'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Printing',
        'Topic :: Software Development :: Bug Tracking',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development :: Testing',
        'Topic :: Terminals',
        'Topic :: Utilities',
    ],
    keywords=[
        'display',
        'print',
        'verbose',
        'context',
        'printer',
        'block',
        'context-printer',
        'debug',
    ],
    python_requires='>=3.8',
    project_urls={
        'Source Repository': 'https://framagit.org/robinechuca/context-verbose/',
        # 'Bug Tracker': 'https://github.com/engineerjoe440/ElectricPy/issues',
        # 'Documentation': 'http://raisin-docs.ddns.net',
        # 'Packaging tutorial': 'https://packaging.python.org/tutorials/distributing-packages/',
        },
    include_package_data=False,
)
