#!/usr/bin/env python

import os

from setuptools import find_packages, setup

requirements = ["pyyaml", "numpy"]

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read().replace(".. :changelog", "")


PACKAGE_PATH = os.path.abspath(os.path.join(__file__, os.pardir))

setup(
    name="ekit",
    version="0.2.5",
    description='Toolbox for the Non-Gaussian Statistics Framework (NGSF)',
    long_description=open('README.rst').read(),
    author="Dominik Zuercher",
    author_email="dominikz@phys.ethz.ch",
    url="https://cosmo-docs.phys.ethz.ch/ekit",
    packages=find_packages(include=["ekit"]),
    include_package_data=True,
    install_requires=requirements,
    license="MIT License",
    zip_safe=False,
    keywords="ekit",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.10",
    ],
)
