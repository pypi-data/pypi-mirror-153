#!/usr/bin/env python
# -*- coding:utf-8 -*-
import inspect
import json
import pathlib as pt

import pandas as pd

from ioproc.logger import datalogger as dlog

__author__ = ["Benjamin Fuchs", "Judith Vesper", "Felix Nitsch"]
__copyright__ = "Copyright 2020, German Aerospace Center (DLR)"
__credits__ = [
    "Niklas Wulff",
    "Hedda Gardian",
    "Gabriel Pivaro",
    "Kai von Krbek",
    "Jan Buschmann",
]

__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Felix Nitsch"
__email__ = "ioProc@dlr.de"
__status__ = "Production"


class DataFieldError(Exception):
    """
    Error message raised from DataManager if the requested data set is not available.
    """

    pass


class DataDict(dict):
    """
    The DataDict is used to serialize data items for a key provided
    """

    def __setitem__(self, key, value):
        if isinstance(value, (pd.DataFrame, pd.Series)):
            super().__setitem__(key, value)
        else:
            raise DataFieldError(
                'The value "{1}" of the dict entry "{0}" has to be a Dataframe or a Series.'.format(key, value)
            )

    def dataSerialize(self, key):
        for ikey, ival in self.items():
            yield "{}/{}".format(key, ikey), ival


class DataManager(dict):
    """
    The DataManager behaves like a dictionary.
    It stores input and output data during run time.
    It makes the data available by their keys and
    can be called at any time in the workflow.
    """

    _overwriteFlag = False

    class __OverwriteProxy:
        """
        Changes the overwriteFlag in the data manager temporarily in order to
        allow overwriting of already existing data sets using 'with' statements.
        """

        def __init__(self, mother):
            self.mother = mother

        def __enter__(self):
            self.mother._overwriteFlag = True
            dlog.debug("activated overwrite of data sets")

        def __exit__(self, exc_type, exc_val, exc_tb):
            dlog.debug("deactivated overwrite of data sets")
            self.mother._overwriteFlag = False

    def __init__(self, run_in_debug_mode, *args, **kwargs):
        """
        Initializes the DataManager with the default dict init.
        Then it sets the additional attribute _overwriteProxy
        """
        super().__init__(*args, **kwargs)
        self._overwriteProxy = self.__OverwriteProxy(self)
        self._actionCfg = None
        self._inAction = False
        self._accessLog = []
        self._run_in_debug_mode = run_in_debug_mode

    @property
    def overwrite(self):
        """
        Is used in a with block, to enable overwrites of data fields in the data manager.
        Otherwise an error is raised.
        :return: the __OverwriteProxy for overwrites
        """
        return self._overwriteProxy

    def entersAction(self, actionCfg):
        """
        Executed when an action will be executed.
        This process registers the action internally and sets the flag _inAction.
        :param actionCfg:
        """
        self._actionCfg = actionCfg
        self._inAction = True

    def leavesAction(self):
        """
        Executed when an action has been processed.
        This process signals the data manager that it can clear the access log and to
        reset the flag _inAction.
        """
        self._actionCfg = None
        self._inAction = False
        self._accessLog.clear()

    def _addToAccessLog(self, dataSetName, modifier):
        """
        Adds a data set to the access log for reporting.
        :param dataSetName: the name of the data set accessed
        :param modifier: the modifier, so read or write access
        """
        assert modifier in ["r", "w",], "access log modifier needs to be read r or write w"
        self._accessLog.append(dataSetName + " (" + modifier + ")")

    def report(self):
        """
        Creates a text report from the access log detailing which
        data sets were accessed and if for read or write purposes.
        :return:
        """
        ret = (
            f'During execution of action "{self._actionCfg["call"]}" (project: "{self._actionCfg["project"]}") '
            f"the following data sets were accessed:\n"
        )
        for i in self._accessLog:
            ret += "    " + i + "\n"
        return ret

    def __setitem__(self, fieldname, dataset):
        """
        Sets the data set specified by field name to value and
        checks if overwrite of existing data fields is enabled.
        Checks also if the field was specified as an output for the action.
        :param fieldname: the field name
        :param dataset: the data set
        """
        errorOccured = False
        if self._actionCfg["call"] not in [
            "checkpoint",
        ]:
            if self._actionCfg["data"]["write_to_dmgr"] is None:
                errorOccured = True
            elif hasattr(self._actionCfg["data"]["write_to_dmgr"], "keys"):
                if fieldname not in self._actionCfg["data"]["write_to_dmgr"].values():
                    errorOccured = True
            elif fieldname not in self._actionCfg["data"]["write_to_dmgr"]:
                errorOccured = True

        if errorOccured:
            if self._run_in_debug_mode:
                dlog.warn(
                    f'the dataset "{fieldname}" was not declared as output for action '
                    f'"{self._actionCfg["call"]}". Please check the workflow specified in the user.yaml!'
                )
            else:
                raise IOError(
                    f'the dataset "{fieldname}" was not declared as output for action '
                    f'"{self._actionCfg["call"]}". Please check the workflow specified in the user.yaml!'
                )

        if self._overwriteFlag:
            dlog.info('overwriting data set "{}"'.format(fieldname))
        assert (
            self._overwriteFlag or fieldname not in self.keys()
        ), 'dataset "{}" already in data manager. ' "Overwrite prohibited. Use with dmgr: block!".format(fieldname)

        dlog.debug("setting field: " + fieldname + "->" + str(dataset))
        self._addToAccessLog(fieldname, "w")

        super().__setitem__(fieldname, dataset)

    def __getitem__(self, fieldname):
        """
        Retrieve data set by field name.
        Checks also if the field was specified as an input for the action.
        :param fieldname:
        """

        errorOccured = False
        if self._actionCfg["call"] not in [
            "checkpoint",
        ]:
            if self._actionCfg["data"]["read_from_dmgr"] is None:
                errorOccured = True
            elif hasattr(self._actionCfg["data"]["read_from_dmgr"], "keys"):
                if fieldname not in self._actionCfg["data"]["read_from_dmgr"].values():
                    errorOccured = True
            elif fieldname not in self._actionCfg["data"]["read_from_dmgr"]:
                errorOccured = True

        if errorOccured:
            if self._run_in_debug_mode:
                dlog.warn(
                    f'the dataset "{fieldname}" was not declared as input for action '
                    f'"{self._actionCfg["call"]}". Please check the workflow specified in the user.yaml!'
                )
            else:
                raise IOError(
                    f'the dataset "{fieldname}" was not declared as input for action '
                    f'"{self._actionCfg["call"]}". Please check the workflow specified in the user.yaml!'
                )

        self._addToAccessLog(fieldname, "r")
        dlog.debug("getting field: " + fieldname)
        try:
            return super().__getitem__(fieldname)
        except KeyError:
            s = inspect.stack()

            actionName = "undefined"
            lineno = "MIA"
            filename = "MIA"
            for idx, iframe in enumerate(s):
                if iframe.function == "__actionwrapper__":
                    last = s[idx - 1]
                    actionName = last.function
                    lineno = last.lineno
                    filename = pt.Path(last.filename).name
                    break

            raise DataFieldError(
                '\n      dataset "{}" unavailable\n'
                '      requested by action "{}" in line {}\n'
                '      in file "{}"'.format(fieldname, actionName, lineno, filename)
            )

    def validate(self, reference, raiseError=True):
        """
        Validate if fields listed in reference exist in the data manager
        :param reference: a list of data field names
        :return: True/False or raises DataFieldError
        """
        hasErrors = False
        errorCode = ""
        for field in reference:
            if field not in self:
                hasErrors = True
                errorCode += " " + field
        if hasErrors and raiseError:
            raise DataFieldError("Missing fields in DataManager: " + errorCode)

        return hasErrors

    def toCache(self, tag):
        """
        Writes the current content of the DataManager (only DataFrames, Series and serializable .json data)
        in .hdf5 format to disc with filename Cache_[tag], so that the work can be resumed at a later point. Overwrites
        existing cache files sharing the same tag.
        :param tag: user specified filename extension
        """
        root_folder = pt.Path(".checkpoint_data")
        root_folder.mkdir(exist_ok=True)

        with pd.HDFStore((root_folder / f"Cache_{tag}.h5f").as_posix(), mode="w") as cache:
            otherData = pd.Series()
            for ikey, ivalue in self.items():
                if isinstance(ivalue, (pd.DataFrame, pd.Series)):
                    cache.put(ikey, ivalue)
                elif hasattr(ivalue, "items"):
                    ivalue = DataDict(ivalue)
                    for k, v in ivalue.dataSerialize(ikey):
                        cache.put(k, v)
                else:
                    try:
                        otherData.loc[ikey] = json.dumps(ivalue)
                    except Exception:
                        otherData.loc[ikey] = "missing"
                        dlog.warning(
                            'Dataset "{}" could not be saved to cache. Unhandled data type "{}"'.format(
                                ikey, type(ivalue)
                            )
                        )
                        dlog.exception()
            cache.put("__otherData", otherData)

    def fromCache(self, tag, iActionInfo):
        """
        Clears the current DataManager, reads the cached data from disc in .hdf5 format
        and loads it into the DataManager.
        :param tag: filename extension of the file to read
        :param iActionInfo: current action to execute
        """
        self.clear()
        self._actionCfg = iActionInfo

        with pd.HDFStore("./.checkpoint_data/Cache_{}.h5f".format(tag), mode="r+") as cache:
            if "__otherData" in cache.keys():
                for ikey, ivalue in cache["__otherData"].items():
                    self[ikey] = json.loads(ivalue)

            for ikey in cache:
                ikey = ikey.lstrip("/")
                if "/" in ikey:
                    key0, key1 = ikey.split("/")
                    if key0 not in self:
                        self[key0] = {}
                    self[key0][key1] = cache[ikey]
                    continue
                if ikey == "__otherData":
                    continue
                self[ikey] = cache[ikey]

    def export_to_dict(self) -> dict:
        """
        exports the current dict of data sets into a fresh one and returns the content.
        Note that no copy of datasets is made.

        :returns: dict instance of datasets
        """
        return dict(self.items())
