# -*- coding: utf-8 -*-

"""IO module.

This module is in charge of data serialization / deserialization to:
    * XLSX format
    * ConfigObj format
"""

import configparser
import logging
import os
import re
from collections import defaultdict
from io import StringIO
from zipfile import ZipFile

import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal

try:
    from configobj import ConfigObj

    IS_CONFIGOBJ = True
except ImportError as exc:
    logging.exception(exc)
    IS_CONFIGOBJ = False

ROW_PREFIX = "_row_"
DEFAULT_EXCEL_ENGINE = "openpyxl"


# from pandas 1.1 pandas.testing.assert_frame_equal.html
PD_SENSIBLE_TESTING = {
    "check_dtype": True,  # bool, default True
    "check_index_type": "equiv",  # bool or {'equiv'}, default 'equiv'
    "check_column_type": "equiv",  # bool or {'equiv'}, default 'equiv'
    "check_frame_type": True,  # bool, default True
    "check_names": True,  # bool, default True
    "by_blocks": False,  # bool, default False
    "check_exact": False,  # bool, default False
    "check_datetimelike_compat": False,  # bool, default False
    "check_categorical": True,  # bool, default True
    "check_like": False,  # bool, default False
    "check_freq": True,  # bool, default True
    "rtol": 1e-5,  # float, default 1e-5
    "atol": 1e-8,  # float, default 1e-8
    "obj": "DataFrame",  # str, default "DataFrame"
}


# =============================================================================
# functional read() methods
# =============================================================================
def _cfg_section_to_df(tabname, data, len_prefix):
    """eg.
    tabname: "names"
    data: {'_row_0': {'id': 1, 'Name': 'Doe', 'Firstname': 'John'}, ...}
    """
    # transform "{ROW_PREFIX}n" -> index
    columns = data.pop("columns", None)
    index = [int(ix[len_prefix:]) for ix in data.keys()]
    if not columns:
        # legacy format without `columns` specifications
        df = pd.DataFrame(data.values(), index=index)
    else:
        df = pd.DataFrame(data.values(), columns=columns.split(","), index=index)
    df = df.replace("", np.nan, regex=False)
    df.columns = [c.replace(":::", "\n") for c in df.columns]
    return df


def read_data(fpath, sheet_name=None, engine=DEFAULT_EXCEL_ENGINE):
    """mimic pandas.read_excel() function"""
    fmts = {
        ".xlsx": (read_excel, {"engine": engine}),
        ".cfg": (read_configobj, {}),
        ".ini": (read_configobj, {}),
    }
    frootname, ext = os.path.splitext(fpath)
    func, kwargs = fmts[ext]
    return func(fpath=fpath, sheet_name=sheet_name, **kwargs)


def read_excel(fpath, sheet_name=None, engine=DEFAULT_EXCEL_ENGINE):
    """read excel file using pandas"""
    df_dict = pd.read_excel(fpath, sheet_name=sheet_name, engine=engine)
    # remove any blank lines
    ret = {k: df.dropna(how="all") for k, df in df_dict.items()}
    # also clean Unnamed columns
    for tab, df in ret.items():
        try:
            df = df[
                [c for c in df if isinstance(c, str) and not c.startswith("Unnamed: ")]
            ]
        except Exception as exc:
            logging.critical(f"cannot parse {tab=}")
            raise
        ret[tab] = df
    return ret


def read_configobj(fpath, as_content=False, sheet_name=None, row_prefix="sniff"):
    ret = {}
    if as_content:
        # fpath **is** the content of the file.
        fpath = StringIO(fpath)
    config = ConfigObj(fpath, indent_type="    ", unrepr=True, write_empty_values=True)
    # transform sections to tabs and data to columns...
    if row_prefix == "sniff":
        try:
            row_prefix = _sniff_row_prefix(config[config.sections[0]].sections[0])
        except IndexError:
            breakpoint()
    else:
        row_prefix = ROW_PREFIX
    for tabname, data in config.items():
        ret[tabname] = _cfg_section_to_df(tabname, data, len(row_prefix))
    # filter out sheet_name
    if sheet_name is None:
        return ret
    elif isinstance(sheet_name, str):
        return ret[sheet_name]
    else:
        raise NotImplementedError("not imp")


def to_configobj(data, fpath=None):
    ret = data.to_configobj(fpath)
    if not fpath:
        ret = "\n".join([s.decode() for s in ret])
    return ret


def to_excel(data, fpath):
    data.to_excel(fpath)
    return fpath


# =============================================================================
# Object wrapper
# =============================================================================


class IOMixin:
    """Input/ouput for grid data"""

    def reset(self):
        """reset container"""
        self._data = {}
        self._units = {}

    # ========================================================================
    # comparisons
    # ========================================================================

    def __eq__(self, other):
        """compare to IO objects"""
        # --------------------------------------------------------------------
        # compare tabnames (order is not important)
        tabs1 = set(self._data.keys())
        tabs2 = set(other._data.keys())
        if tabs1 != tabs2:
            return False
        # --------------------------------------------------------------------
        # for each tabname, compare dataframes using sensible defaults
        for tabname, df in self._data.items():
            try:
                assert_frame_equal(df, other._data[tabname], **PD_SENSIBLE_TESTING)
            except AssertionError:
                return False
        return True

    def compare(self, other, **kwargs):
        """compare two IO containers"""
        # --------------------------------------------------------------------
        # compare tabnames (order is not important)
        tabs1 = set(self._data.keys())
        tabs2 = set(other._data.keys())
        missing = tabs1 ^ tabs2
        if missing:
            logging.warning("missing tabs in one or other: %s", missing)
        # --------------------------------------------------------------------
        # keep common tabnames ordered as in self
        settings = PD_SENSIBLE_TESTING.copy()
        settings.update(**kwargs)
        tabs = tabs1 & tabs2
        tabs = [tabname for tabname in tabs1 if tabname in tabs]
        for tabname in tabs:
            sdf = self._data[tabname]
            odf = other._data[tabname]
            try:
                assert_frame_equal(sdf, odf, **settings)
            except AssertionError as exc:
                logging.warning('tabname "[%s]"', tabname)
                logging.warning(exc)
                logging.warning("**left**:\n%s", sdf)
                logging.warning("**right**:\n%s", odf)

    def to(self, fpath):
        """write to the given file, guessing format from the extension"""
        fmts = {
            ".xlsx": self.to_excel,
            ".cfg": self.to_configobj,
            ".ini": self.to_configobj,
        }
        ext = os.path.splitext(fpath)[1]
        return fmts[ext](fpath)

    def read(self, fpath, engine=DEFAULT_EXCEL_ENGINE):
        """write to the given file, guessing format from the extension"""
        fmts = {
            ".xlsx": (self.read_excel, {"engine": engine}),
            ".cfg": (self.read_configobj, {}),
            ".ini": (self.read_configobj, {}),
        }
        frootname, ext = os.path.splitext(fpath)
        func, kwargs = fmts[ext]
        return func(fpath=fpath, **kwargs)

    # ========================================================================
    # EXCEL io
    # ========================================================================

    def read_excel(self, fpath, sheet_name=None, engine=DEFAULT_EXCEL_ENGINE):
        """read excel-like file and store all the tabs
        as pandas DataFrame values"""
        self.reset()
        self._data = read_excel(fpath, sheet_name=sheet_name, engine=engine)

    def to_excel(self, fpath):
        with pd.ExcelWriter(fpath) as writer:
            for tabname, df in self._data.items():
                df.to_excel(writer, sheet_name=tabname, index=False)
        return fpath

    # ========================================================================
    # CONFIGOBJ io
    # ========================================================================
    def read_configobj(self, fpath, sheet_name=None, row_prefix="sniff"):
        if not IS_CONFIGOBJ:
            raise ValueError(
                "Cannot export to configobj. Please install configobj before"
            )
        self.reset()
        self._data = read_configobj(fpath, sheet_name=sheet_name)

    def to_configobj(self, fpath=None):
        """write data as a config obj two-levels nested file"""
        if not IS_CONFIGOBJ:
            raise ValueError(
                "Cannot export to configobj. Please install configobj before"
            )
        config = ConfigObj(
            indent_type="    ", unrepr=True, write_empty_values=True, encoding="utf-8"
        )
        if not fpath:
            config.filename = None
        for tabname, df in self._data.items():
            try:
                units = self.getunits(tabname)
            except KeyError:
                units = {}
            if units:
                # insert units row
                units = pd.Series(units).to_frame().T
                df = pd.concat((units, df), ignore_index=True)
            df = df.fillna("")
            df2dict = df.T.to_dict()
            config[tabname] = {}  # create a section
            config[tabname]["columns"] = ",".join(df.columns.tolist())
            for id_, id_data in df2dict.items():
                # multiline headers are not allowed
                id_data = {k.replace("\n", ":::"): v for k, v in id_data.items()}
                config[tabname][f"{ROW_PREFIX}{id_}"] = id_data
        if not fpath:
            config.filename = None
            txt = config.write()
            return txt
        else:
            config.filename = fpath
            config.write()
            return fpath

    # # ========================================================================
    # # INI files to
    # # ========================================================================
    # def to_inifiles(self, fpath):
    #     """write data as a bunch of ini files zipped in a dir"""
    #     nb_total = len(self._data)
    #     # --------------------------------------------------------------------
    #     # meta_dict config file handle data types
    #     meta_dict = {} # defaultdict(dict)

    #     # with ZipFile(fpath, "a") as zipini:
    #     #     zipini.writestr("META.cfg", ", ".join(list(self._data.keys())))
    #     # --------------------------------------------------------------------
    #     # create one ini file per tab
    #     for i, (tabname, df) in enumerate(self._data.items()):
    #         df = df.fillna("")
    #         df2dict = df.T.to_dict()
    #         # ----------------------------------------------------------------
    #         # create ini's content
    #         config = configparser.RawConfigParser()
    #         config.optionxform = lambda option: option
    #         for id_, id_data in df2dict.items():
    #             config[f"{ROW_PREFIX}{id_}"] = id_data
    #         # write data in a dummy file
    #         fp = StringIO()
    #         config.write(fp)
    #         fp.seek(0)
    #         with ZipFile(fpath, "a") as zipini:
    #             zipini.writestr("%s.ini" % tabname, fp.read())
    #         # ----------------------------------------------------------------
    #         # append metadata
    #         meta_dict[tabname] = {'types': df.dtypes.to_dict()}
    #     __import__('pdb').set_trace()
    #     meta = configparser.RawConfigParser()
    #     meta.optionxform = lambda option: option
    #     with ZipFile(fpath, "a") as zipini:
    #         zipini.writestr("META.cfg", ", ".join(list(self._data.keys())))
    #     return fpath

    # def read_inifiles(self, fpath, row_prefix="sniff"):
    #     if not os.path.isfile(fpath):
    #         raise FileNotFoundError(fpath)
    #     with ZipFile(fpath, "r") as zipini:
    #         # read tabs order:
    #         with zipini.open("TOC.txt") as tocf:
    #             toc = [tabname.strip() for tabname in tocf.read().decode().split(",")]
    #         for tabname in toc:
    #             fname = tabname + ".ini"
    #             with zipini.open(fname) as fh:
    #                 content = fh.read().decode()
    #             data = configparser.RawConfigParser()
    #             data.optionxform = lambda option: option
    #             data.read_string(content)
    #             if row_prefix == "sniff":
    #                 row_prefix = _sniff_row_prefix(data.sections()[0])
    #             else:
    #                 row_prefix = ROW_PREFIX
    #             data = dict(data.items())
    #             # still one level to expand
    #             data = {k: dict(v.items()) for k, v in data.items() if k != "DEFAULT"}
    #             if tabname == 'names':
    #                 __import__('pdb').set_trace()
    #             df = _cfg_section_to_df(tabname, data, len(row_prefix))
    #             self._data[tabname] = df


def _sniff_row_prefix(sec_title):
    return re.match(r"^(.*)\d+$", sec_title).group(1)
