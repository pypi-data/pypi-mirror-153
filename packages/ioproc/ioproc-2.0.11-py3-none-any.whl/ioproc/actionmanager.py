#!/usr/bin/env python
# -*- coding:utf-8 -*-
import importlib.util
import os
import pathlib as pt
import sys

from ioproc.config import configProvider

__author__ = ["Benjamin Fuchs", "Judith Vesper", "Felix Nitsch"]
__copyright__ = "Copyright 2020, German Aerospace Center (DLR)"
__credits__ = ["Niklas Wulff", "Hedda Gardian", "Gabriel Pivaro", "Kai von Krbek"]

__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Felix Nitsch"
__email__ = "ioProc@dlr.de"
__status__ = "Production"


class ActionError(Exception):
    """
    Error raised by the ActionManager
    """

    pass


class ActionManager(dict):
    """
    Behaves like a dictionary and stores the project name and the action name together with a reference to the action.
    """

    def __setitem__(self, key, value):
        """
        overloaded method to handle two level keys.
        :param key: a tuple containing the project name and the action name
        :param value: the reference to an action
        """
        projectName, actionName = key

        if projectName not in self:
            super().__setitem__(projectName, {})

        if actionName in self[projectName]:
            raise ActionError("Action {} already registered.".format(actionName))

        self[projectName][actionName] = value


class __actioninit:
    """
    Asserts that only one ActionManager instance exists in the framework (Singleton).
    Within the framework, getActionManager is called to get a new ActionManager instance.
    getActionManager is an instance of the __actioninit class. On calling the getActionManager
    a check is done, if an ActionManager was already created. In this case the ActionManager
    instance is returned. If there is no instantiated ActionManager, a new instance is created
    and populated with actions.
    """

    actionMgr = None

    def __call__(self, config=None):
        """
        A call of the class __actioninit checks if an action manager instance is already available. (callable class)
        If no, it instantiates and populates a new one.
        If yes, it returns the previously created instance.
        :return: populated ActionManager instance
        """
        if self.actionMgr is None:
            self.actionMgr = ActionManager()
            if config is None:
                config = configProvider.get()

            p = os.path.abspath(
                config["user_yaml_path"].parent / config["user"]["action_folder"]
            )
            sys.path.append(p)
            action_folder_path = pt.Path(p)

            for ifile in action_folder_path.glob("./*.py"):
                spec = importlib.util.spec_from_file_location(
                    f"actions.{ifile.name.strip('.py')}", ifile.as_posix()
                )
                __m = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(__m)

            for imodule in action_folder_path.glob("./*/__init__.py"):
                module_name = imodule.parent.name
                for ifile in imodule.parent.glob("./**/*.py"):
                    spec = importlib.util.spec_from_file_location(
                        f"actions.{module_name}.{ifile.name.strip('.py')}",
                        ifile.as_posix(),
                    )
                    __m = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(__m)

        return self.actionMgr


getActionManager = __actioninit()
