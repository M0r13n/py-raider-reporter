"""
py-raider-reporter
Copyright 2020, Leon Morten Richter
Author: Leon Morten Richter <leon.morten@gmail.com>
"""

import os
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

VERSION = None
with open(os.path.join('raider_reporter', '__init__.py')) as f:
    for line in f:
        if line.strip().startswith('__version__'):
            VERSION = line.split('=')[1].strip()[1:-1].strip()
            break


setup(
    name='py-raider-reporter',
    version=VERSION,
    description='Raider Reporter for Python',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Leon Morten Richter',
    author_email='leon.morten@gmail.com',
    url='https://github.com/M0r13n/py-raider-reporter',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        "requests"
    ]
)
