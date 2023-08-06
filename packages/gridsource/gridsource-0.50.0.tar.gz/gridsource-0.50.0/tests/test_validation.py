#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `gridsource` package."""

import os
import shutil
from pprint import pprint as pp

import numpy as np
import pandas as pd
import pytest

from gridsource import Data as IVData
from gridsource import ValidData as VData
from gridsource.validation import DataFrameSchematizer, ureg


def test_DFS_00_schema_bulding():
    """test DataFrameSchematizer class.
    DataFrameSchematizer class is purely internal and wrapped by VData or IVData
    """
    v = DataFrameSchematizer()
    columns_specs = """\
---
id:
  types: integer
  unique: true
  mandatory: true
name:
  types: string
  mandatory: true
firstname:
  types: string
age:
  types: integer
  minimum: 0
life_nb:
  types: integer
  mandatory: true
  maximum: 4
"""
    v.add_columns(columns_specs)
    # build valid jsonschema
    schema = v.build()
    expected_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "properties": {
            "age": {
                "items": {
                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                    "minimum": 0,
                },
                "type": "array",
                "uniqueItems": False,
            },
            "firstname": {
                "items": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                "type": "array",
                "uniqueItems": False,
            },
            "id": {"items": {"type": "integer"}, "type": "array", "uniqueItems": True},
            "life_nb": {
                "items": {"maximum": 4, "type": "integer"},
                "type": "array",
                "uniqueItems": False,
            },
            "name": {
                "items": {"type": "string"},
                "type": "array",
                "uniqueItems": False,
            },
        },
        "required": ["id", "name", "life_nb"],
        "type": "object",
    }

    assert schema == expected_schema


def test_DFS_01_validation():
    """test DataFrameSchematizer class validation.
    DataFrameSchematizer class is purely internal and wrapped by VData or IVData


    This test-case mainly check **default** values on a simple one-row dataframe

    | Value        | default | mandatory | result    | check |
    |--------------+---------+-----------+-----------+-------|
    | blank or nan |         | True      | FAIL      | da    |
    | blank or nan |         | False     | blank nan | db    |
    | blank or nan | 1       | True      | FAIL      | dc    |
    | blank or nan | 1       | False     | 1         | dd    |
    | 2            |         | True      | 2         | de    |
    | 2            |         | False     | 2         | df    |
    | 2            | 1       | True      | 2         | dg    |
    | 2            | 1       | False     | 2         | dh    |
    """
    v = DataFrameSchematizer()
    columns_specs = """\
---
da:
  types: integer
  mandatory: true
db:
  types: integer
  mandatory: false
dc:
  types: integer
  mandatory: true
  default: 1
dd:
  types: integer
  mandatory: false
  default: 1
de:
  types: integer
  mandatory: true
df:
  types: integer
  mandatory: false
dg:
  types: integer
  mandatory: true
  default: 1
dh:
  types: integer
  mandatory: false
  default: 1
"""
    v.add_columns(columns_specs)
    df = pd.DataFrame(
        {
            "da": {1: None},
            "db": {},
            "dc": {1: np.nan},
            "dd": {1: None},
            "de": {1: 2},
            "df": {1: 2},
            "dg": {1: 2},
            "dh": {1: 2},
        }
    )
    df, is_valid, errors = v.validate_dataframe(df)
    assert is_valid is False
    expected_errors = {
        ("da", 0): ["None is not of type 'integer'"],
        ("dc", 0): ["None is not of type 'integer'"],
    }
    assert errors == expected_errors
    # check that values have been correctly filled
    expected_data = {
        "da": {0: None},
        "db": {0: np.nan},
        "dc": {0: 1},
        "dd": {0: 1},
        "de": {0: 2},
        "df": {0: 2},
        "dg": {0: 2},
        "dh": {0: 2},
    }
    expected_df = pd.DataFrame(expected_data)
    assert pd.testing.assert_frame_equal(df, expected_df, check_dtype=False) is None


def test_DFS_02_validation():
    """test DataFrameSchematizer class validation.
    specifically testing enums with default
    """
    columns_specs = """\
---
CA:
  types: integer
  default: 0
  units: m
CB:
  types: number
  default: 1.0
CC:
  types: number
  default: 1.0
CD:
  types: number
  default: 0
  units: N
CE:
  types: string
  enum:
    - fwd
    - aft
  default: aft
CF:
  types: number
  default: 0
  units: kg
"""
    v = DataFrameSchematizer()
    v.add_columns(columns_specs)
    df = pd.DataFrame(
        {
            "CA": {0: "cm", 1: 5, 2: 15},
            "CB": {0: "", 1: 5.3},  # empty units specified, but that's fine
            "CC": {1: 5.3},  # no units specified, but that's fine
            "CD": {1: 54.3},  # no units specified, that's an issue!
            "CE": {1: "fwd"},
            "CF": {0: "lbm", 1: 2},  # "lbm" doesn't exist
        }
    )
    df, is_valid, errors = v.validate_dataframe(df)
    assert errors == {
        ("CD", None): ["no units specified in source file"],
        ("CF", None): ["undefined units 'lbm'"],
    }
    # let's correct the previous errors
    v = DataFrameSchematizer()
    v.add_columns(columns_specs)

    df = pd.DataFrame(
        {
            "CA": {0: "cm", 1: 5, 2: 15},
            "CB": {0: "", 1: 5.3},  # empty units specified, but that's fine
            "CC": {1: 5.3},  # no units specified, but that's fine
            "CD": {0: "lbf", 1: 54.3},  # no units specified, that's an issue!
            "CE": {1: "fwd"},
            "CF": {0: "lb", 1: 2},  # "lbm" doesn't exist
        }
    )
    df, is_valid, errors = v.validate_dataframe(df)
    assert errors == {}
    exp = pd.DataFrame(
        {
            "CA": {0: 0.05, 1: 0.15},
            "CB": {0: 5.3, 1: 1.0},
            "CC": {0: 5.3, 1: 1.0},
            "CD": {0: 241.53843370864516, 1: 0.0},
            "CE": {0: "fwd", 1: "aft"},
            "CF": {0: 0.9071847400000002, 1: 0.0},
        }
    )
    assert pd.testing.assert_frame_equal(df, exp) is None


def test_VData_00():
    data = VData()
    # ------------------------------------------------------------------------
    # Create a schema for "test" tab
    # This example show a YAML schema syntax,
    # but json or plain dict is also OK:
    from io import StringIO

    data._set_schema(
        "test",
        "---"
        "\nid:"
        "\n  types: integer"
        "\n  unique: true"
        "\n  mandatory: true"
        "\nname:"
        "\n  types: string"
        "\n  mandatory: true"
        "\nfirstname:"
        "\n  types: string"
        "\nage:"
        "\n  types: integer"
        "\n  minimum: 0"
        "\nlife_nb:"
        "\n  types: integer"
        "\n  mandatory: true"
        "\n  maximum: 4",
    )
    # ------------------------------------------------------------------------
    # create dummy data
    data._data["test"] = pd.DataFrame(
        {
            "id": {7: 0, 1: 1, 2: 1},
            "name": {7: "Doe", 1: "Fante", 2: "Mercury"},
            "firstname": {7: "John", 2: "Freddy", 1: "Richard"},
            "age": {7: "42", 1: 22},
            "life_nb": {7: 5, 1: "hg", 2: 15},
        }
    )
    expected_report = {
        ("age", 0): [
            "'42' is not valid under any of the given schemas",
            "'42' is not of type 'integer'",
            "'42' is not of type 'null'",
        ],
        ("id", "?"): ["value {1} is not unique"],
        ("life_nb", 0): ["5 is greater than the maximum of 4"],
        ("life_nb", 1): ["'hg' is not of type 'integer'"],
        ("life_nb", 2): ["15 is greater than the maximum of 4"],
    }
    df, is_valid, errors = data._validate_tab("test")
    assert is_valid is False
    assert errors == expected_report


# =============================================================================
# level 1 : read files on disk
# =============================================================================


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


def test_IVData_00(datadir):
    indir, outdir = datadir
    data = IVData()
    data.read_excel(os.path.join(indir, "test_00.xlsx"))
    data.read_schema(os.path.join(indir, "test_00.schema.yaml"))
    for tab in ("names", "cars", "empty"):
        print('checking "%s"' % tab, end="... ")
        df, is_ok, errors = data._validate_tab(tab)
        assert is_ok is True
        assert errors == {}
    # ------------------------------------------------------------------------
    # export and reimport to/from various formats
    for extension in (".cfg", ".xlsx", ".ini"):
        target = os.path.join(outdir, "test_00" + extension)
        print("test '%s' extension" % target)
        assert not os.path.isfile(target)
        data.to(target)
        assert os.path.isfile(target)
        # --------------------------------------------------------------------
        # read the newly created file
        data_new = IVData()
        data_new.read(target)
        data_new.read_schema(os.path.join(indir, "test_00.schema.yaml"))
        for tab in data._data.keys():
            print('checking "%s"' % tab, end="... ")
            df, is_ok, errors = data_new._validate_tab(tab)
            try:
                assert is_ok is True
            except:
                print("OUPS!")
            else:
                print("OK")
            assert errors == {}


def test_IVData_01(datadir):
    indir, outdir = datadir
    data = IVData()
    data.read_excel(os.path.join(indir, "test_00.xlsx"))
    data.read_schema(os.path.join(indir, "test_00.schema.yaml"))
    ret = data.validate()
    assert len(ret) == 0


def test_IVData_02(datadir):
    indir, outdir = datadir
    data = IVData()
    data.read_excel(os.path.join(indir, "test_00.xlsx"))
    data.read_schema(os.path.join(indir, "test_00.schema2.yaml"))
    # default row reporting as "data"
    ret = data.validate()
    assert ret == {
        "cars": {("Year", 3): ["None is not of type 'integer'"]},
        "names": {"general": ["'name' is a required property"]},
    }
    ret = data.validate(10)
    assert ret == {
        "cars": {("Year", 12): ["None is not of type 'integer'"]},
        "names": {"general": ["'name' is a required property"]},
    }
    ret = data.validate("spreadsheet")
    assert ret == {
        "cars": {("Year", 4): ["None is not of type 'integer'"]},
        "names": {"general": ["'name' is a required property"]},
    }


def test_IVData_03(datadir):
    """make schema a bit more complex: add generic keys"""
    indir, outdir = datadir
    data = IVData()
    data.read_excel(os.path.join(indir, "test_02.xlsx"))
    data.read_schema(os.path.join(indir, "test_02.schema.yaml"))
    ret = data.validate("data")
    print(ret)  # TODO: remove me!
    assert len(ret) == 2
    expected_errors = {
        "names": {"general": ["'life_nb' is a required property"]},
        "french_cars": {
            ("brand", 3): [
                "'Citroën' is not one of ['Peugeot', 'Toyota', 'Ford', 'Renault']"
            ]
        },
    }

    assert ret == expected_errors


def test_IVData_04(datadir):
    """check units"""
    indir, outdir = datadir
    data = IVData()
    data.read(os.path.join(indir, "test_03_units.ini"))
    # -------------------------------------------------------------------------
    # read and check schema
    data.read_schema(os.path.join(indir, "test_03_units.schema.yaml"))
    expected_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "properties": {
            "Volume": {
                "items": {
                    "anyOf": [{"type": "number"}, {"type": "null"}],
                    "default": 0,
                },
                "type": "array",
                "uniqueItems": False,
                "units": "m^3",
            },
            "distA": {
                "items": {"type": "number"},
                "type": "array",
                "uniqueItems": False,
                "units": "m",
            },
            "distB": {
                "items": {
                    "anyOf": [{"type": "number"}, {"type": "null"}],
                    "default": 0,
                },
                "type": "array",
                "uniqueItems": False,
                "units": "m",
            },
            "id": {"items": {"type": "integer"}, "type": "array", "uniqueItems": True},
        },
        "required": ["id", "distA"],
        "type": "object",
    }
    assert data._schemas["geom"].build() == expected_schema
    ret = data.validate("spreadsheet")
    expected_geom = pd.DataFrame(
        {
            "id": {0: 1.0, 1: 2.0},
            "distA": {0: 0.0010000000000000005, 1: 0.002000000000000001},
            "distB": {0: 14.3, 1: 15.0},
            "Volume": {0: 1.5064562386943998, 1: 0.8183568665087998},
        }
    )
    actual_geom = data._data["geom"]
    assert pd.testing.assert_frame_equal(actual_geom, expected_geom) is None


def test_IVData_05_failing_units(datadir):
    """check units"""
    indir, outdir = datadir
    data = IVData()
    data.read(os.path.join(indir, "test_04_units_failing.xlsx"))
    # -------------------------------------------------------------------------
    # read and check schema
    data.read_schema(
        os.path.join(indir, "test_04_IMP.yaml"),
        os.path.join(indir, "test_04_data.yaml"),
    )
    # -------------------------------------------------------------------------
    # test tabname present in schemas, but not in data
    whatever = data._schemas["whatever"].build()
    assert whatever == {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "properties": {
            "force": {
                "items": {"anyOf": [{"type": "integer"}, {"type": "null"}]},
                "type": "array",
                "uniqueItems": False,
                "units": "lbf",
            },
            "length": {
                "items": {
                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                    "default": 0,
                },
                "type": "array",
                "uniqueItems": False,
                "units": "in",
            },
            "mass": {
                "items": {"anyOf": [{"type": "integer"}, {"type": "null"}]},
                "type": "array",
                "uniqueItems": False,
                "units": "lb",
            },
            "pressure": {
                "items": {"anyOf": [{"type": "integer"}, {"type": "null"}]},
                "type": "array",
                "uniqueItems": False,
                "units": "psi",
            },
            "volume": {
                "items": {"anyOf": [{"type": "integer"}, {"type": "null"}]},
                "type": "array",
                "uniqueItems": False,
                "units": "in^3",
            },
        },
        "required": [],
        "type": "object",
    }

    expected_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "properties": {
            "test_volume_foot3": {
                "items": {"type": "number"},
                "type": "array",
                "uniqueItems": False,
                "units": "in^3",
            },
            "test_volume_foot³": {
                "items": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                "type": "array",
                "uniqueItems": False,
                "units": "in^3",
            },
            "test_volume_ft³": {
                "items": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                "type": "array",
                "uniqueItems": False,
                "units": "in^3",
            },
            "test_volume_in3": {
                "items": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                "type": "array",
                "uniqueItems": False,
                "units": "in^3",
            },
            "test_volume_m3": {
                "items": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                "type": "array",
                "uniqueItems": False,
                "units": "in^3",
            },
            "test_volume_m³": {
                "items": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                "type": "array",
                "uniqueItems": False,
                "units": "in^3",
            },
        },
        "required": ["test_volume_foot3"],
        "type": "object",
    }

    assert data._schemas["volume"].build() == expected_schema
    ret = data.validate("data")
    expected_report = {
        "mass": {
            ("test_mass_g", 3): ["None is not of type 'number'"],
            ("test_mass_lbm", None): ["undefined units 'lbm'"],
        },
        "volume": {"general": ["'test_volume_foot3' is a required property"]},
    }
    assert expected_report == ret


def test_IVData_06_units(datadir):
    """check units"""
    indir, outdir = datadir
    data_imp = IVData()
    data_imp.read(os.path.join(indir, "test_04_units.xlsx"))
    # -------------------------------------------------------------------------
    # read and check schema
    data_imp.read_schema(
        os.path.join(indir, "test_04_IMP.yaml"),
        os.path.join(indir, "test_04_data.yaml"),
    )
    expected_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "properties": {
            "test_volume_foot3": {
                "items": {"type": "number"},
                "type": "array",
                "uniqueItems": False,
                "units": "in^3",
            },
            "test_volume_foot³": {
                "items": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                "type": "array",
                "uniqueItems": False,
                "units": "in^3",
            },
            "test_volume_ft³": {
                "items": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                "type": "array",
                "uniqueItems": False,
                "units": "in^3",
            },
            "test_volume_in3": {
                "items": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                "type": "array",
                "uniqueItems": False,
                "units": "in^3",
            },
            "test_volume_m3": {
                "items": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                "type": "array",
                "uniqueItems": False,
                "units": "in^3",
            },
            "test_volume_m³": {
                "items": {"anyOf": [{"type": "number"}, {"type": "null"}]},
                "type": "array",
                "uniqueItems": False,
                "units": "in^3",
            },
        },
        "required": ["test_volume_foot3"],
        "type": "object",
    }

    assert data_imp._schemas["volume"].build() == expected_schema
    ret = data_imp.validate()
    assert ret == {}  # no errors found
    # for each tab, all the values of each row shall be the same
    data_SI = IVData()
    data_SI.read(os.path.join(indir, "test_04_units.xlsx"))
    # -------------------------------------------------------------------------
    # read and check schema
    data_SI.read_schema(
        os.path.join(indir, "test_04_SI.yaml"),
        os.path.join(indir, "test_04_data.yaml"),
    )
    data_SI.validate()
    data_imp.quantify("volume")
    for tabname in data_imp._data:
        df_imp = data_imp.convert_to(tabname)  # .pint.to_base_units()
        df_si = data_SI.convert_to(tabname)  # .pint.to_base_units()
        assert (
            pd.testing.assert_frame_equal(
                df_imp.pint.dequantify(), df_si.pint.dequantify()
            )
            is None
        )
    # -------------------------------------------------------------------------
    # getunits
    assert data_SI.getunits("pressure", key="test_p_bar") == "MPa"
    assert data_imp.getunits("pressure", key="test_p_bar") == "psi"
    # column length/id has no units:
    with pytest.raises(KeyError):
        data_imp.getunits("length", key="id")
    # getvalue
    l9 = data_SI.getrow("length", key=9, search_by="id")
    l9_expected = pd.Series(
        {
            "test_dist_m": 2000,
            "test_dist_yd": 2000,
            "test_dist_in": 2000,
            "test_dist_ft": 2000,
            "test_dist_foot": 2000,
            "test_string": "a",
            "groucho": 3.2,
        },
        name=9.0,
    )
    assert pd.testing.assert_series_equal(l9, l9_expected) is None

    l9_value = data_SI.getvalue(
        "length", key=9, search_by="id", column="test_dist_yd", as_quantity=False
    )
    assert pytest.approx(l9_value) == 2000

    l9_quantity_exp = 2 * ureg.m
    # rendering with quantity:
    l9_quantity = data_SI.getvalue(
        "length", key=9, search_by="id", column="test_dist_yd"
    )
    diff = l9_quantity - l9_quantity_exp
    assert abs(diff.magnitude) < 1e-5
    # -------------------------------------------------------------------------
    # to_configobj
    co = data_imp.to_configobj()
    new_data = IVData()
    new_data.read_configobj(co)
    new_data.read_schema(
        os.path.join(indir, "test_04_IMP.yaml"),
        os.path.join(indir, "test_04_data.yaml"),
    )
    new_data.validate()
    assert new_data.getunits("pressure", key="test_p_bar") == "psi"
    for tabname in data_imp._data:
        df_imp = data_imp.convert_to(tabname)  # .pint.to_base_units()
        df_new_data = new_data.convert_to(tabname)  # .pint.to_base_units()
        exp = df_imp.pint.dequantify()
        act = df_new_data.pint.dequantify()
        assert pd.testing.assert_frame_equal(exp, act) is None


def test_IVData_07_failing_units(datadir):
    """check units"""
    indir, outdir = datadir
    data_si = IVData()
    data_si.read(os.path.join(indir, "test_05_units_failing.xlsx"))
    # -------------------------------------------------------------------------
    # read and check schema
    data_si.read_schema(
        os.path.join(indir, "test_05_SI.yaml"),
        os.path.join(indir, "test_05_data.yaml"),
    )
    rep = data_si.validate()
    assert rep == {
        "mass": {
            "general": [
                "'test_mass_tonne' is a required property",
                "'test_mass_g' is a required property",
            ],
            ("test_mass_lb", 1): [
                "'a' is not valid under any of the given " "schemas",
                "'a' is not of type 'number'",
                "'a' is not of type 'null'",
            ],
            ("test_mass_lb", "?"): "cannot convert some values to numeric",
        }
    }


def test_IVData_08_multi_cols_uniqueness(datadir):
    """check units"""
    indir, outdir = datadir
    data_si = IVData()
    data_si.read(os.path.join(indir, "test_06_multi-columns_uniqueness.ini"))
    # -------------------------------------------------------------------------
    # read and check schema
    data_si.read_schema(
        os.path.join(indir, "test_05_SI.yaml"),
        os.path.join(indir, "test_06_data.yaml"),
    )
    rep = data_si.validate()
    assert rep == {
        "WithPadding_failing": {
            ("rail_tag & x_loc & block_label", "?"): [
                "value {'RBL12 & 3800.0 & s1'} is not unique"
            ]
        },
        "asm_failing": {
            ("another", "?"): ["value {1.0} is not unique"],
            ("rail_tag & x_loc & block_label", "?"): [
                "value {'RBL11 & 3500.0 & RECARO1'} is not unique"
            ],
        },
    }
    df = data_si.get("WithPadding_ok")
    expected_df = pd.DataFrame(
        {
            0: {
                "another": 1.0,
                "block_label": "RECARO1",
                "block_ref_point_id": 2.0,
                "optional": 2.0,
                "rail_tag": "RBL11",
                "x_loc": 3500.0,
            },
            1: {
                "another": 2.0,
                "block_label": "RECARO1",
                "block_ref_point_id": 2.0,
                "optional": 3.0,
                "rail_tag": "RBL11",
                "x_loc": 8500.0,
            },
            2: {
                "another": 3.0,
                "block_label": "s1",
                "block_ref_point_id": 2.0,
                "optional": np.nan,
                "rail_tag": "RBL12",
                "x_loc": 3800.0,
            },
            3: {
                "another": 4.0,
                "block_label": "s2",
                "block_ref_point_id": 2.0,
                "optional": 0.0,
                "rail_tag": "RBL12",
                "x_loc": 3800.0,
            },
            4: {
                "another": 5.0,
                "block_label": "s1",
                "block_ref_point_id": 2.0,
                "optional": np.nan,
                "rail_tag": "RBL12",
                "x_loc": 8500.0,
            },
            5: {
                "another": 6.0,
                "block_label": "s1",
                "block_ref_point_id": 2.0,
                "optional": np.nan,
                "rail_tag": "RBL12",
                "x_loc": 7900.0,
            },
        }
    ).T
    expected_df = expected_df[[c for c in df]]
    assert pd.testing.assert_frame_equal(df, expected_df, check_dtype=False) is None


def test_IVData_09_must_exist_in(datadir):
    """check 'must exist' and 'must not exist' req"""
    indir, outdir = datadir
    data = IVData()
    data.read_excel(os.path.join(indir, "test_06_must_exist_in.xlsx"))
    data.read_schema(os.path.join(indir, "test_06_must_exist_in.yaml"))
    ret = data.validate("spreadsheet")
    expected_errors = {
        "beams": {
            ("beam_id", 5): ["'value `6.0` not found in `beam_def::id`"],
            ("color_id", 7): [
                "'a' is not of type 'integer'",
                "'value `a` not found in `colors::id`",
            ],
        },
        "colors": {
            ("id", 2): ["'value `1` unexpectidely found in `beam_def::id`"],
            ("id", 4): ["'tata' is not of type 'integer'"],
            ("name", 4): ["5 is not of type 'string'"],
        },
    }

    assert ret == expected_errors


def test_IVData_10_mandatory_if(datadir):
    """check 'mandatory_if' req"""
    indir, outdir = datadir
    data = IVData()
    data.read_excel(os.path.join(indir, "test_10_mandatory_if.xlsx"))
    data.read_schema(os.path.join(indir, "test_10_mandatory_if.yaml"))
    ret = data.validate("spreadsheet")
    expected_errors = {
        "beams": {
            ("beam_id", 5): ["'value `6.0` not found in `beam_def::id`"],
            ("color_id", 7): [
                "'a' is not of type 'integer'",
                "'value `a` not found in `colors::id`",
            ],
        },
        "colors": {
            ("blue_subtype", 6): "This value is mandatory for `id>3`",
            ("blue_subtype", 7): "This value is mandatory for `id>3`",
            ("blue_subtype", 8): "This value is mandatory for `id>3`",
            ("id", 2): ["'value `1` unexpectidely found in `beam_def::id`"],
            ("id", 5): ["'value `4` unexpectidely found in `beam_def::id`"],
            ("red_subtype", 4): "This value is mandatory for `name=='red'`",
        },
    }
    assert ret == expected_errors


def test_IVData_11_empty_tab(datadir):
    indir, outdir = datadir
    data = IVData()
    data.read_excel(os.path.join(indir, "test_11.xlsx"))
    data.read_schema(os.path.join(indir, "test_11.schema.yaml"))
    for tab in ("names", "cars", "empty"):
        print('checking "%s"' % tab, end="... ")
        df, is_ok, errors = data._validate_tab(tab)
        assert is_ok is True
        assert errors == {}
    # ------------------------------------------------------------------------
    # export and reimport to/from various formats
    for extension in (".xlsx", ".ini"):
        target = os.path.join(outdir, "test_00" + extension)
        print("test '%s' extension" % target)
        assert not os.path.isfile(target)
        data.to(target)
        assert os.path.isfile(target)
        # --------------------------------------------------------------------
        # read the newly created file
        data_new = IVData()
        data_new.read(target)
        data_new.read_schema(os.path.join(indir, "test_11.schema.yaml"))
        for tab in data._data.keys():
            print('checking "%s"' % tab, end="... ")
            df, is_ok, errors = data_new._validate_tab(tab)
            try:
                assert is_ok is True
            except:
                print("OUPS!")
            else:
                print("OK")
            assert errors == {}
