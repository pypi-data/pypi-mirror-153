#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = ["Benjamin Fuchs", "Judith Vesper", "Felix Nitsch"]
__copyright__ = "Copyright 2020, German Aerospace Center (DLR)"
__credits__ = ["Niklas Wulff", "Hedda Gardian", "Gabriel Pivaro", "Kai von Krbek"]

__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Felix Nitsch"
__email__ = "ioProc@dlr.de"
__status__ = "Production"


"""
This file features several default scripts for setting up and testing ioProc.
"""

defaultRunPyFile = """
#-*- coding:utf-8 -*-


import ioproc.runners as run

run.start()
"""

defaultSetupFoldersPyFile = """
#-*- coding:utf-8 -*-


import ioproc.runners as run

run.create_folders()
"""

defaultUserContent = """actionFolder: ../../actions

debug:
  time_it: False
  enable_development_mode: False

from_check_point: start

workflow:
    # configure your workflow here
"""

defaultActions = r"""
#-*- coding:utf-8 -*-

from enum import Enum

import pandas as pd

import pathlib as pt
import subprocess as spr
import tempfile

from ioproc.tools import action
from ioproc.logger import mainlogger


@action('general')
def execute(dmgr: dict, config: dict, params: dict):
    '''
    executes an executable program on this local computer.

    :param dmgr:
    :param config:
    :param params:
    :return: nothing
    '''

    args = [params['executable'], ]

    provided_args = list(params.get('args', []))

    args.extend(provided_args)

    shell = params.get('shell', False)
    cwd = params.get('cwd', pt.Path.cwd().as_posix())

    mainlogger.info('executing ', *args)
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpdirname = pt.Path(tmpdirname)
        std = tmpdirname / 'stdout.dat'
        err = tmpdirname / 'errout.dat'
        with std.open('w') as stdoutF:
            with err.open('w') as erroutF:
                try:
                    status = spr.run(args, stdout=stdoutF, stderr=erroutF,
                                     shell=shell, cwd=cwd,
                                     encoding='utf-8', text=True,
                                     )
                except FileNotFoundError as exc:
                    if not shell:
                        mainlogger.error('maybe the error is related to shell=False. Please read the subprocess '
                                         'package documentation on the "shell" parameter for the function "run"'
                                         'for more information.')
                    raise exc

        mainlogger.info(f"executed {params['args']['executable']}")
        if status.returncode == 0:
            mainlogger.info('successfully')

            with std.open('r') as ipf:
                data = ipf.read()
            mainlogger.info(data)
        else:
            with std.open('r') as ipf:
                data = ipf.read()
            mainlogger.info(data)
            with err.open('r') as ipf:
                data = ipf.read()
            mainlogger.error('with errors!')
            mainlogger.error(data)



@action('general')
def print_data(dmgr, config, params):
    '''
    simple debugging printing function. Prints all data in the data manager.

    Does not have any parameters.
    '''
    for k, v in dmgr.items():
        mainlogger.info(k+' = \n'+str(v))


@action('general')
def checkpoint(dmgr, config, params):
    '''
    creates a checkpoint file in the current working directory with name
    Cache_TAG while TAG is supplied by the action config.

    :param tag: the tag for this checkpoint, this can never be "start"
    '''
    assert params['tag'] != 'start', 'checkpoints can not be named start'
    dmgr.toCache(params['tag'])
    mainlogger.info('set checkpoint "{}"'.format(params['tag']))


@action('general')
def parse_excel(dmgr, config, params):
    '''
    Parses given `excelFile` for specified `excelSheets` as dataframe object and stores it in the datamanager by the
    key specified in `write_to_dmgr`.
    `excelHeader` can be set to `True` or `False`.

    The action may be specified in the user.yaml as follows:
        - action:
            project: general
            call: parse_excel
            data:
              read_from_dmgr: null
              write_to_dmgr: parsedData
            args:
              excelFile: spreadsheet.xlsx
              excelSheet: sheet1
              excelHeader: True
    '''

    args = params['args']
    file = get_field(args, 'excelFile')
    excel_sheet = get_excel_sheet(args)
    header = get_header(get_field(args, 'excelHeader'))
    parsed_excel = pd.read_excel(io=file, sheet_name=excel_sheet, header=header)

    with dmgr.overwrite:
        dmgr[params['data']['write_to_dmgr']] = parsed_excel


def get_field(dictionary, key):
    ''' Returns value from given `dictionary` and raises `KeyError` if `key` is not specified '''
    try:
        return dictionary[key]
    except KeyError:
        message = "Missing key '{}'. Given keys are '{}'.".format(key, [key for key in dictionary.keys()])
        raise KeyError(message)


def get_excel_sheet(params):
    ''' Returns a list of excel_sheets to parse from given dictionary or raises error when field is not specified '''
    try:
        return get_field(params, 'excelSheet')
    except KeyError:
        message = "Please specify the Excel sheet(s) to parse in a list using under the field `excelSheets`."
        raise IOError(message)


class Header(Enum):
    TRUE = 0
    FALSE = None


def get_header(string):
    ''' Returns converted operator from given bool '''
    header_map = {True: Header.TRUE.value,
                  False: Header.FALSE.value,
                  }
    return header_map[string]
"""

defaultConfigContent = """
userschema: schema/user_schema.yaml
"""
