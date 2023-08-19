#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='python_libs',
    version='0.8.1',
    description="""Testt""",
    long_description="Long description",
    author='Luis Carlos Berrocal',
    author_email='luis.berrocal.1942@gmail.com',
    url='https://github.com/luiscberrocal/py-understanding',
    packages=[
        'python_libs',
    ],
    include_package_data=True,
    # install_requires=requirements,
    zip_safe=False,
    keywords='python_libs',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Not open source',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    entry_points={
        'console_scripts': [
            'py-rich=pj_kafka_wrapper.cli.cli_cmd:main',
        ],
    },
)
