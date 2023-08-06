#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = ["Benjamin Fuchs"]
__copyright__ = "Copyright 2021, German Aerospace Center (DLR)"
__credits__ = []

__license__ = "MIT"
__version__ = "1.0.2"
__maintainer__ = "Felix Nitsch"
__email__ = "ioProc@dlr.de"
__status__ = "Production"


class UnknownActionModule(Exception):
    pass


class UnknownAction(Exception):
    pass


class CheckPointError(Exception):
    pass


class ActionParamsError(Exception):
    pass


class MissingOverridesError(Exception):
    pass
