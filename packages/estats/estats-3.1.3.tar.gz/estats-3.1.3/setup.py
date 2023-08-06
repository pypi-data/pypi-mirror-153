#!/usr/bin/env python

import os
from setuptools import find_packages, setup

requirements = ['numpy', 'healpy', 'tqdm', 'matplotlib', 'ekit', 'scipy',
                'astropy', 'pandas', 'tensorflow', 'keras', 'scikit-learn']

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read().replace(".. :changelog", "")


PACKAGE_PATH = os.path.abspath(os.path.join(__file__, os.pardir))

setup(
    name="estats",
    version="3.1.3",
    description="The building blocks of the Non-Gaussian Statistics Framework",
    long_description=open('README.rst').read(),
    author="Dominik Zuercher",
    author_email="dominikz@phys.ethz.ch",
    url="https://cosmo-docs.phys.ethz.ch/estats",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=requirements,
    license="MIT License",
    zip_safe=False,
    keywords="estats",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.10",
    ],
)
