#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='dfn',
    version='1.0.1',
    author='yifei.gao',
    author_email='yifei.gao@sophgo.com',
    description='download_from_nas',
    packages=['dfn'],
    install_requires=["requests","tqdm"]
)