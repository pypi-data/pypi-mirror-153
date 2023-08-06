#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import pathlib as pt

from ioproc.driver import setupworkflow, setupfolders, execute


__author__ = ["Benjamin Fuchs"]
__copyright__ = "Copyright 2020, German Aerospace Center (DLR)"
__credits__ = [
    "Felix Nitsch",
    "Judith Vesper",
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


envPath = pt.Path()

pathvar = os.environ["PATH"]
elem = pathvar.split(";")

for ielem in elem:
    if "Scripts" in ielem:
        envPath = pt.Path(ielem).parent
        break


def create_folders(workflowName="yourTestWorkflow"):
    """
    Creates the required folder structure.
    """
    setupfolders(workflowName)


def create_workflow(path=pt.Path.cwd()):
    """
    Creates a new workflow in the current work directory.
    """
    setupworkflow(path)


def start(useryaml=None):
    """
    Executes the workflow manager.
    """
    execute(useryaml)
