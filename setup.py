#!/usr/bin/env python
from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))


with open(path.join(here, "requirements.txt")) as f:
    requirements = f.read().splitlines()


with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="github-auto-release",
    version="beta",
    python_requires=">=3.5, <4",
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "new-release=auto_release:auto_release",
            "sentry-release=sentry_release:sentry_release",
        ]
    },
)
