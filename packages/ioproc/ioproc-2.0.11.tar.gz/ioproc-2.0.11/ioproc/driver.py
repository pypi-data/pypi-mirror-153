#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import pathlib as pt

import arrow as ar
import click

from ioproc.actionmanager import getActionManager
from ioproc.config import configProvider
from ioproc.datamanager import DataManager
from ioproc.defaults import defaultConfigContent, defaultRunPyFile, defaultUserContent
from ioproc.exceptions import CheckPointError, UnknownAction, UnknownActionModule
from ioproc.logger import datalogger as dlog
from ioproc.logger import mainlogger as log
from ioproc.tools import freeze, humanize_time, setupFolderStructure

__author__ = ["Benjamin Fuchs", "Judith Vesper", "Felix Nitsch"]
__copyright__ = "Copyright 2020, German Aerospace Center (DLR)"
__credits__ = ["Niklas Wulff", "Hedda Gardian", "Gabriel Pivaro", "Kai von Krbek"]

__license__ = "MIT"
__version__ = "1.0.2"
__maintainer__ = "Felix Nitsch"
__email__ = "ioProc@dlr.de"
__status__ = "Production"


IOPROCINSTALLROOT = pt.Path(__file__).resolve().parent
SCHEMAPATH = pt.Path(IOPROCINSTALLROOT, "schema")
HOME = pt.Path.home()

defaultConfigContent = defaultConfigContent.format(IOPROCINSTALLROOT.as_posix())


@click.group()
@click.pass_context
def ioproc(ctx):
    ctx.ensure_object(dict)


@ioproc.command(help="setup default folder structure")
@click.option("--workflowname", default="workflow1", help="name of your workflow")
def setupfolders(workflowname):
    setupFolderStructure(workflowname)


@ioproc.command(help="create all necessary files for workflow in current folder or at userconfig location")
@click.option("--path", "-p", default=None, help="path to folder where to create workflow")
def setupworkflow(path):
    path = pt.Path.cwd() if path is None else pt.Path(path)
    if not path.exists():
        raise IOError(f"workflow folder not found: {path.as_posix()}")

    p = path / "user.yaml"
    if not p.exists():
        with p.open("w") as opf:
            opf.write(defaultUserContent)

    p = path / "run.py"
    if not p.exists():
        with p.open("w") as opf:
            opf.write(defaultRunPyFile)


def format_override(ctx, self, s):
    try:
        d = tuple(i.strip().split("=") for i in s)
        d = dict(d)
    except Exception:
        raise click.exceptions.BadArgumentUsage("the overwrites need to be of shape: ioproc overwrites a=1 b=2")

    return d


@ioproc.command(help="execute ioproc workflow defined by user.yaml in current folder")
@click.option("--useryaml", "-u", default=None, help="path to user.yaml")
@click.option(
    "--override/--no-override", "-o", default=False, help="override values of the user.yaml (based on jinja2 syntax)",
)
@click.argument("overridedata", nargs=-1, callback=format_override)
def execute(useryaml, override, overridedata):

    if override and not overridedata:
        raise click.exceptions.ClickException("Missing override data")
    elif not override and overridedata:
        raise click.exceptions.ClickException("overrides need to be specified with ioproc execute -o")

    _execute(useryaml, overridedata=overridedata, return_data=False)


def _execute(path_to_user_yaml: pt.Path, overridedata: [dict, None] = None, return_data: bool = False,) -> [dict, None]:
    start = ar.now()

    if overridedata is None:
        overridedata = {}

    userConfigPath = pt.Path(pt.Path.cwd(), "user.yaml")

    if path_to_user_yaml is not None:
        userConfigPath = pt.Path(path_to_user_yaml)

    old_pwd = pt.Path.cwd()

    os.chdir(userConfigPath.parent.as_posix())
    userConfigPath = userConfigPath.relative_to(userConfigPath.parent)

    try:
        data = _execute_workflow(userConfigPath, overridedata, return_data)
    finally:
        os.chdir(old_pwd.as_posix())
        end = ar.now()
        log.info(f"run duration: {humanize_time(end-start)}")

    if return_data:
        return data


def _execute_workflow(userConfigPath, overridedata, return_data):

    configProvider.setPathes(userConfigPath=userConfigPath,)

    config = configProvider.get(overridedata)

    log, dlog = _setup_workflow_logger(config)

    actionMgr = getActionManager(config)
    assert (
        len(actionMgr) > 0
    ), "ActionManager is not defined. Ensure 'actionFolder' path in 'user.yaml' is set correctly."
    dmgr = DataManager(config["user"]["debug"]["enable_development_mode"])

    log.info("starting workflow")

    log.debug("commencing action calling")

    FROM_CHECK_POINT = config["user"]["from_check_point"] != "start"
    IGNORE_CHECK_POINTS = False
    if "ignore_check_points" in config["user"]:
        IGNORE_CHECK_POINTS = config["user"]["ignore_check_points"]

    if IGNORE_CHECK_POINTS:
        FROM_CHECK_POINT = False

    _validate_workflow_actions(config, actionMgr)

    CHECK_POINT_DEFINED_IN_WORKFLOW = False

    if FROM_CHECK_POINT:
        _check_for_checkpoint_data(config)

    for iActionInfo in config["user"]["workflow"]:
        iActionInfo = iActionInfo[list(iActionInfo.keys())[0]]
        if FROM_CHECK_POINT:
            if "tag" in iActionInfo and iActionInfo["tag"] == config["user"]["from_check_point"]:
                FROM_CHECK_POINT = False
                CHECK_POINT_DEFINED_IN_WORKFLOW = True
                dmgr.fromCache(config["user"]["from_check_point"], iActionInfo)
                log.info('reading from cache for tag "{}"'.format(config["user"]["from_check_point"]))
            continue
        log.debug('executing action "' + iActionInfo["call"] + '"')
        dmgr.entersAction(iActionInfo)

        if IGNORE_CHECK_POINTS and iActionInfo["call"] == "checkpoint":
            log.warning(f'skipping checkpoint "{iActionInfo["tag"]}" due to "ignore check points" option set to true')
            continue

        try:
            actionMgr[iActionInfo["project"]][iActionInfo["call"]](dmgr, config, freeze(iActionInfo))
        except Exception as e:
            log.exception(
                'Fatal error during execution of action "'
                + iActionInfo["call"]
                + '":\nData manager log:\n'
                + dmgr.report()
            )
            raise e
        dmgr.leavesAction()

    if not CHECK_POINT_DEFINED_IN_WORKFLOW and FROM_CHECK_POINT:
        raise CheckPointError(
            f'The requested checkpoint "{config["user"]["from_check_point"]}" ' f"is not defined in the workflow!"
        )

    if return_data:
        return dmgr.export_to_dict()


def _check_for_checkpoint_data(config):
    given_tag = config["user"]["from_check_point"]
    if not pt.Path("./.checkpoint_data/Cache_{}.h5f".format(given_tag)).is_file():
        message = (
            f"cannot find cache file with given tag name '{given_tag}' "
            f" in './.checkpoint_data/Cache_{given_tag}.h5f'"
        )
        log.exception(message)
        raise Exception(message)


def _setup_workflow_logger(config):
    if "debug" in config["user"] and "log_level" in config["user"]["debug"]:
        log.setLevel(config["user"]["debug"]["log_level"])
        dlog.setLevel(config["user"]["debug"]["log_level"])
    else:
        log.setLevel("INFO")
        dlog.setLevel("INFO")
    return log, dlog


def _validate_workflow_actions(config, actionMgr):
    # this is a cross check loop to identify early problems in the workflow.
    for iActionInfo in config["user"]["workflow"]:
        iActionInfo = iActionInfo[list(iActionInfo.keys())[0]]
        if iActionInfo["project"] not in actionMgr:
            raise UnknownActionModule(
                f'The action module "{iActionInfo["project"]}" is not known to ioproc.\n'
                f'please check in the action folder for it: "{config["user"]["action_folder"]}"'
            )

        if iActionInfo["call"] not in actionMgr[iActionInfo["project"]]:
            raise UnknownAction(
                f'The action "{iActionInfo["call"]}" is not known to ioproc.\n'
                f'please check in the action folder "{config["user"]["action_folder"]}"\n'
                f'in the module {iActionInfo["project"]} for the action.'
            )


if __name__ == "__main__":
    ioproc()
