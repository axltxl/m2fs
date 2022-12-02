#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
setuptools config file
"""

from setuptools import setup, find_packages
from midi2sim import __version__ as version
from midi2sim import __author__ as author
from midi2sim import PKG_URL as pkg_url
from midi2sim import __name__ as pkg_name


desc = "Fly on any SimConnect-compatible simulators using your MIDI controllers"

# CONTINUE HERE TOMORROW
setup(
    name=pkg_name,
    version=version,
    packages=find_packages(),
    author=author,
    author_email="me@axltxl.xyz",
    description=desc,
    url=pkg_url,
    license="MIT",
    download_url="{url}/tarball/{version}".format(url=pkg_url, version=version),
    keywords=["simconnect"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console	",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        "console_scripts": [
            "midi2sim = midi2sim.__main__:main",
        ],
    },
)
