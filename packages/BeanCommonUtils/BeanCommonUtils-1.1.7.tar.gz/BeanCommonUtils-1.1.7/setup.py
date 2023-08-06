# -*- coding: UTF-8 -*-

from __future__ import print_function
from setuptools import setup, find_packages

setup(
    name="BeanCommonUtils",
    version="1.1.7",
    author="Hly",
    author_email="hlyaction@gmail.com",
    description="A Python library for common methods.",
    long_description=open("README.rst", encoding='gb18030', errors='ignore').read(),
    license="MIT",
    url="https://github.com/beansKingdom/CommonUtils",
    packages=find_packages(),
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "DBUtils",
    ]
)
