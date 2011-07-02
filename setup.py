#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
import os

def read_file(*path):
    base_dir = os.path.dirname(__file__)
    file_path = (base_dir, ) + tuple(path)
    return file(os.path.join(*file_path)).read()

setup(
    name = "flask-cn",
    url = "http://flask.flyzen.com",
    license="BSD",
    author = "Young King",
    author_email = "yanckin@gmail.com",
    description = "Flask documents (chinese translation)",
    long_description = (
        read_file("README") + "\n\n"),
    version = "0.7",
    packages = [],
    include_package_data = True, 
    zip_safe=False,
    install_requires=['Flask',],
    classifiers = [
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
