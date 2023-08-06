# -*- coding: utf-8 -*-

"""Top-level package for GridSource."""

from gridsource.io import IOMixin
from gridsource.validation import ValidatorMixin

__author__ = """Nicolas Cordier"""
__email__ = "nicolas.cordier@numeric-gmbh.ch"
__version__ = "0.50.0"


class _Base:
    def __init__(self):
        self._data = {}
        possible_mixins_init = ("validator_mixin_init", "io_mixin_init")
        for f in possible_mixins_init:
            if hasattr(self, f):
                getattr(self, f)()

    def get(self, tabname=None, attr="_data"):
        if not attr.startswith("_"):
            attr = "_" + attr
        if not tabname:
            raise AttributeError(f"`tabname` should be one of {set(self._data.keys())}")
        return getattr(self, attr)[tabname]

    def tabs(self, ordered=False):
        """return contained tabs"""
        if not ordered:
            return set(getattr(self, "_data").keys())
        return list(getattr(self, "_data").keys())


class Data(_Base, IOMixin, ValidatorMixin):
    pass


class ValidData(_Base, ValidatorMixin):
    pass


class IOData(_Base, IOMixin):
    pass
