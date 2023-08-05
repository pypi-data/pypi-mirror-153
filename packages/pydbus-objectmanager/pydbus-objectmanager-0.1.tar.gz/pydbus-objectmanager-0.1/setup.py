#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

setup(
	name="pydbus-objectmanager",
	version="0.1",
	description="DBus.ObjectManager implementation for pydbus",
	long_description=long_description,
	long_description_content_type="text/markdown",
	# original author: Sébastien Corne, sebastien@seebz.net
	author="Christian Andersen",
	author_email="christian@milindur.de",
	url="https://github.com/milindur/pydbus-objectmanager",
	license="WTFPL",

	packages=["pydbus_objectmanager"],
	install_requires=["pydbus>=0.6"]
)
