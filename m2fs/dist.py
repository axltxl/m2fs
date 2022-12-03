# -*- coding: utf-8 -*-

try:
    from ._version import __version__

    PKG_VERSION = __version__
except ImportError:
    PKG_VERSION = "dev"

PKG_NAME = "m2fs"
PKG_AUTHOR = "Alejandro Ricoveri"
PKG_URL = f"github.com/axltxl/{PKG_NAME}"
