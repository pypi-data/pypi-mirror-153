#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `gridsource` package."""

import os
import shutil

import pandas as pd
import pytest

from gridsource import Data


@pytest.fixture
def datadir():
    """
    Basic IO Structure
    """
    test_dir = os.path.dirname(os.path.realpath(__file__))
    indir = os.path.join(test_dir, "data")
    outdir = os.path.join(test_dir, "_out")
    # ensure outdir exists and is empty
    if os.path.isdir(outdir):
        shutil.rmtree(outdir)
    os.makedirs(outdir)
    return indir, outdir


def test_00_read_xlsx(datadir):
    """Sample pytest test function with the pytest fixture as an argument."""
    indir, outdir = datadir
    data = Data()
    data.read_excel(os.path.join(indir, "test_00.xlsx"))
    # ------------------------------------------------------------------------
    # test we created a dict...
    assert isinstance(data._data, dict)
    # ------------------------------------------------------------------------
    # ... with relevalt keys
    assert list(data._data.keys()) == ["names", "cars", "empty"]
    assert data.tabs() == {"empty", "names", "cars"}
    assert data.tabs(ordered=True) == ["names", "cars", "empty"]
    # ------------------------------------------------------------------------
    # and pandas IOFrames as values
    for tabname, _d in data._data.items():
        assert isinstance(_d, pd.DataFrame)


def test_01_xlsx_to_configobj(datadir):
    """read one single XLSX source, save to all allowed formats and
    re-read saved files
    """
    indir, outdir = datadir
    data = Data()
    data.read_excel(os.path.join(indir, "test_00.xlsx"))
    # ------------------------------------------------------------------------
    # write using lambda "to"
    for extension in (".cfg", ".xlsx", ".ini"):
        target = os.path.join(outdir, "test_00" + extension)
        print("test '%s' extension" % target)
        assert not os.path.isfile(target)
        data.to(target)
        assert os.path.isfile(target)
        # --------------------------------------------------------------------
        # read the newly created file
        data_new = Data()
        data_new.read(target)
        cmp = data_new.compare(data)
        assert data_new == data
