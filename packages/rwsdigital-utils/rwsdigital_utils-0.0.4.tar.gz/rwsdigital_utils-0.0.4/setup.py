# setup.py

import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

setup(
    name="rwsdigital_utils",
    version="0.0.4",
    description="Odoo development utils",
    readme="README.md",
    author="Salvatore Castaldo",
    author_email = "salvatore@rwsdigital.com",
    license="MIT License",
    url = "https://github.com/sCast17/rwsdigital_utils",
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    )
