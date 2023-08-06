#!/usr/bin/env python
# encoding: utf-8
from setuptools import find_packages, setup

# Package meta-data.
NAME = 'maxtest'
DESCRIPTION = 'maxtest'
URL = 'https://github.com/nevergiveupzsj/maxtest'
EMAIL = '1105522860@qq.com'
AUTHOR = 'Sunbz'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.0.1'

# What packages are required for this module to be executed?
REQUIRED = ["numpy", "matplotlib", "sqlalchemy", "polygon", "pandas"]

# Setting.
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    install_requires=REQUIRED,
    license="MIT"
)
