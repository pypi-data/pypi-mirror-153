#!/usr/bin/env python
# -*- coding:utf-8 -*-
from . import tools
from . import actionmanager
from . import datamanager
from . import logger
from . import defaults
from . import runners
from . import driver


__author__ = [
    "Benjamin Fuchs",
]
__copyright__ = "Copyright 2020, German Aerospace Center (DLR)"
__credits__ = [
    "Judith Vesper",
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


def run():
    driver.ioproc()
