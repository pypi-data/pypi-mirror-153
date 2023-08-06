#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='navinfo_tool',
    version='0.0.5',
    description=(
        'utils for nlp'
    ),
    author='navinfo_nlp',
    author_email='navinfo_nlp@163.com',
    license='Apache License 2.0',
    packages=find_packages(),
    install_requires=[
        'xlrd==1.2.0',
        'jieba',
        'xlwt',
        'xlutils',
        'matplotlib',
        'sklearn',
        'pandas',
        'fairies',
        'configparser',
        'tqdm'
    ],
)
