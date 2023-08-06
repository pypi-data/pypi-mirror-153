# -*- coding:UTF-8 -*-
#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="airflow_util_dv",
    version="2.6.4",
    author="boxue liu",
    author_email="liu.boxue@detvista.com",
    license="Apache License",
    url="https://github.com/boxueliu/airflow_util",
    packages=["airflow_util_dv"],
    install_requires=["cx_Oracle <= 7.1.2 ", "traceback2 <= 1.4.0", "apache-airflow <= 2.2.3", "configparser ==3.5.3"],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6"
    ],
)
