#!/usr/bin/env python
import re
import ast

from setuptools import setup, find_packages


requires = ['python-dotenv>=0.13.0', 'boto3>=1.14.0', 'docker>=5.0.0',  'PyCryptodome >=3.9.8', 'argcomplete>=1.12.3', 'tabulate']

with open('README.md') as readme_file:
    README = readme_file.read()

setup(
    name='cognicept-shell',
    version='1.4.2',
    description='Shell utility to configure Cognicept tools.',
    long_description_content_type="text/markdown",
    long_description=README,
    author='Jakub Tomasek',
    url='https://cognicept.systems',
    packages=find_packages(),
    install_requires=requires,
    license="Apache License 2.0",
    entry_points = {
        'console_scripts': ['cognicept=cogniceptshell.interface:main'],
    },
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8'
    ),
)