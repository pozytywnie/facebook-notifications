#!/usr/bin/env python
from setuptools import find_packages
from setuptools import setup

def read(name):
    from os import path
    return open(path.join(path.dirname(__file__), name)).read()

setup(
    name='facebook-notifications',
    version='3.0.0',
    description="Sends notifications using Facebook Notification API",
    long_description=read("README.rst"),
    maintainer="Tomasz Wysocki",
    maintainer_email="tomasz@wysocki.info",

    install_requires=(
        'facepy>=0.8.2',
    ),
    packages=find_packages(),
)
