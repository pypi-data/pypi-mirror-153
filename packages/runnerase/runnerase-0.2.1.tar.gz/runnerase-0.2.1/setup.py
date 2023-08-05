#!/usr/bin/env python3
# encoding: utf-8
"""Installation configuration.

Even though setup.cfg and pyproject.toml are eventually going to replace
setup.py entirely, at the moment this file is still required to ensure older
pip versions can handle local installations properly. See also
[here](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html).
"""
from setuptools import setup

setup()
