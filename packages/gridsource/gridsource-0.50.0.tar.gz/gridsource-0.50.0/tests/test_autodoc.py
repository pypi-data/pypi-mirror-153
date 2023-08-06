import os
import shlex
import shutil
import subprocess
import tempfile
from io import StringIO
from pathlib import Path

import pytest

from gridsource import Data as IVData
from gridsource.autodoc import VDataAutodoc
from gridsource.validation import load_yaml


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


def test_00(datadir):
    """test autodoc"""
    indir, outdir = datadir
    ivdata = IVData()
    ivdata.read_schema(
        os.path.join(indir, "ftools_example_units.yaml"),
        os.path.join(indir, "ftools_example.yaml"),
    )
    # with tempfile.TemporaryDirectory() as tmpdirname:
    #     ad = VDataAutodoc(ivdata, target_dir=Path(tmpdirname)/"DOC")
    target_dir = Path(tempfile.mkdtemp()) / "test_autodoc"
    ad = VDataAutodoc(ivdata, target_dir=target_dir)
    try:
        ad.create(
            project_name="totor",
            author="me",
            version="1.2",
            exist_ok=False,
        )
    except FileExistsError:
        pass
    ad.dump_data(
        skip_tabs=("default_units",),
        drop_columns=("pattern", "example"),
        rename_columns={
            "dimensionality": "dim",
            "minimum": "min",
            "maximum": "max",
        },
    )
    # -------------------------------------------------------------------------
    # check make html works
    prev_cwd = os.getcwd()
    os.chdir(target_dir)
    ret = subprocess.run(["/usr/bin/make", "html"], shell=True)
    assert ret.returncode == 0
    os.chdir(prev_cwd)
