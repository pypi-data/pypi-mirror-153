#!/usr/bin/env python

import os

from setuptools import find_packages, setup


requirements = ['numpy', 'pyyaml', 'portalocker', 'argparse',
                'ekit']  # during runtime


with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read().replace(".. :changelog", "")


PACKAGE_PATH = os.path.abspath(os.path.join(__file__, os.pardir))

setup(
    name="esub-epipe",
    version="1.9.1",
    description=("Easy-to-use job Scheduler for Python code"),
    long_description=open('README.rst').read(),
    author='Dominik Zuercher',
    author_email='dominik.zuercher@phys.ethz.ch',
    url='https://cosmo-docs.phys.ethz.ch/esub',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license="MIT License",
    zip_safe=False,
    keywords="esub, epipe",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        'console_scripts': [
            "esub = esub.esub:main", "epipe = esub.epipe:main"
        ]
    }
)
