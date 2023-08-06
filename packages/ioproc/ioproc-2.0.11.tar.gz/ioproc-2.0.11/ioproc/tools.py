#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pathlib as pt
import shutil
from functools import wraps

import arrow as ar
import yaml

from ioproc.actionmanager import getActionManager
from ioproc.datamanager import DataManager
from ioproc.defaults import defaultActions, defaultRunPyFile, defaultSetupFoldersPyFile, defaultUserContent
from ioproc.logger import mainlogger as log
from ioproc.exceptions import ActionParamsError


__author__ = ["Benjamin Fuchs", "Judith Vesper", "Kai von Krbek"]
__copyright__ = "Copyright 2020, German Aerospace Center (DLR)"
__credits__ = [
    "Felix Nitsch",
    "Niklas Wulff",
    "Hedda Gardian",
    "Gabriel Pivaro",
    "Kai von Krbek",
]

__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Felix Nitsch"
__email__ = "ioProc@dlr.de"
__status__ = "Production"


def setupFolderStructure(workflowName=""):
    """
    Set up folder structure, which is required for use of the ioProc workflow manager.
    If path already exists, a warning is raised.
    """
    if workflowName.strip() == "":
        workflowName = "workflow1"

    workflowName = workflowName.replace(" ", "_")

    CWD = pt.Path.cwd()

    path2actions = pt.Path(CWD, "actions", "general.py")
    path2workflow = pt.Path(CWD, "workflows", workflowName)
    path2userConfig = pt.Path(path2workflow, "user.yaml")

    path2actions.parent.mkdir(parents=True, exist_ok=True)
    path2workflow.mkdir(parents=True, exist_ok=True)

    if path2userConfig.exists():
        log.warning(f"UserConfig already exists at location {path2userConfig}")
    else:
        try:
            with path2userConfig.open("w") as opf:
                opf.write(defaultUserContent)

            with path2userConfig.open("r") as ipf:
                d = yaml.load(ipf, Loader=yaml.SafeLoader)

            with path2userConfig.open("w") as opf:
                d["actionFolder"] = path2actions.parent.as_posix()
                yaml.dump(d, opf)
        except Exception as e:
            shutil.rmtree(path2userConfig.as_posix())
            raise e

    if path2actions.exists():
        log.warning(f"General.py already exists at location {path2actions.parent}")
    else:
        with path2actions.open("w") as opf:
            opf.write(defaultActions)

    root = pt.Path().cwd()
    folderScript = root / "create_folder_structure.py"
    if not folderScript.exists():
        with folderScript.open("w") as opf:
            opf.write(defaultSetupFoldersPyFile)

    workflowStartScript = path2workflow / "run.py"
    if not workflowStartScript.exists():
        with workflowStartScript.open("w") as opf:
            opf.write(defaultRunPyFile)


class action:
    def __init__(self, project):
        """
        decorator to register actions in the ActionManager and validate input
        :param project: name of project
        """
        self.projectName = project

    def __call__(self, f):
        actionMgr = getActionManager()

        @wraps(f)
        def __actionwrapper__(dmgr, config, params):
            log.debug("calling wrapper")

            if type(dmgr) != DataManager:
                raise TypeError("no valid dataManager instance passed")

            start = ar.now()

            try:
                ret = f(dmgr, config, params)
            except Exception as e:
                log.exception(f'Error occured calling action "{self.projectName}-{f.__name__}"')
                raise e

            end = ar.now()
            log.info(f"duration '{self.projectName}.{f.__name__}': {end - start}")
            return ret

        actionMgr[self.projectName, f.__name__] = __actionwrapper__

        log.debug("wrapping complete for action: " + str(__actionwrapper__.__name__))
        return __actionwrapper__


class ActionArgs(dict):
    def __init__(self, *args, **kwargs):
        self.parents = kwargs.pop('parents', ())
        if len(self.parents) == 0:
            self.parents = ""
        else:
            self.parents = 'under section [' + "][".join(self.parents) + '] '
        
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        if key in self:
            return super().__getitem__(key)

        message = "Parameter '{}' is not a valid action input. Possible action input parameter/s {}is/are {}. Please check the user.yaml.".format(key, self.parents, list(self.keys()))
        raise ActionParamsError(message)
   
    def __setitem__(self, key, value):
        raise TypeError('Action arguments are read only.')


def freeze(d, parents=None):
    """
    This function converts a given dictionary in a read-only mapping, also called frozen-dictionary.
    :return a frozen dictionary where a key cannot be added nor removed
    """
    if parents is None:
        parents = tuple()

    for key, value in d.items():
        if not hasattr(value, "lstrip") and not hasattr(value, "items") and hasattr(value, "__iter__"):
            d[key] = tuple(value)
        elif hasattr(value, "items"):
            new_parents = list(parents)
            new_parents.append(key) 
            new_parents = tuple(new_parents)
            d[key] = freeze(value, new_parents)
    return ActionArgs(d, parents=parents)


def humanize_time(dt):
    # based on: https://raimasoftware.com/how-to-humanize-date-and-time-in-python
    # get the interval from the < dt > to the current moment in seconds
    interval = int(dt.total_seconds())

    # edge case of < dt> is now
    if interval == 0:
        return f"{round(dt.total_seconds(), 2)} ms"
    else:
        interval = -interval

    names = ["second", "minute", "hour", "day", "week", "month", "year"]
    multipliers = [
        1,
        60,
        3600,
        3600 * 24,
        3600 * 24 * 7,
        3660 * 24 * 30,
        3660 * 24 * 30 * 12,
    ]

    pretty = ""

    for i, m in enumerate(multipliers[::-1]):
        value = interval // m
        interval -= value * m
        if value == 0:
            pass
        elif value == 1:
            pretty += f"{value} {names[-(i+1)]} "
        else:
            pretty += f"{value} {names[-(i+1)]}s "
    return pretty
