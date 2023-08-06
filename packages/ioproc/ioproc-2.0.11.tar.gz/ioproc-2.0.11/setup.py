# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ioproc']

package_data = \
{'': ['*']}

install_requires = \
['Cerberus>=1.3.2,<2.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'arrow>=1.1.0,<2.0.0',
 'click>=8.0.1,<9.0.0',
 'frozendict>=2.0.2,<3.0.0',
 'jinja2>=3.0.0,<4.0.0',
 'pandas>=1.2.4,<2.0.0',
 'tables>=3.5.1,<4.0.0']

entry_points = \
{'console_scripts': ['ioproc = ioproc:run']}

setup_kwargs = {
    'name': 'ioproc',
    'version': '2.0.11',
    'description': 'Framework for data pre- and postprocessing - ioProc is a light-weight workflow manager for Python ensuring robust, scalable and reproducible data pipelines. The tool is developed at the German Aerospace Center (DLR) for and in the scientific context of energy systems analysis, however, it is widely applicable in other scientific fields.',
    'long_description': '[![PyPI version](https://badge.fury.io/py/ioproc.svg)](https://badge.fury.io/py/ioproc)\n[![PyPI license](https://img.shields.io/pypi/l/ioproc.svg)](https://badge.fury.io/py/ioproc)\n[![pipeline status](https://gitlab.dlr.de/ioproc/ioproc/badges/development/pipeline.svg)](https://gitlab.dlr.de/ioproc/ioproc/-/commits/development)\n[![coverage report](https://gitlab.dlr.de/ioproc/ioproc/badges/development/coverage.svg)](https://gitlab.dlr.de/ioproc/ioproc/-/commits/development) \n\n# The ioProc workflow manager\n`ioproc` is a light-weight workflow manager for Python ensuring robust, scalable and reproducible data pipelines. The tool is developed at the German Aerospace Center (DLR) for and in the scientific context of energy systems analysis, however, it is widely applicable in other scientific fields.\n\n## how-to install\nSetup a new Python environment and install ioProc using \n\n    pip install ioproc   \n\n## how-to configure\n\nConfigure your pipeline in the `user.yaml`. The `workflow` is defined by a list of actions. These must\ncontain the fields `project`, `call` and `data` (with sub fields `read_from_dmgr`, and `write_to_dmgr`). The user\nmay specify additional fields for each action under the optional key `args`.  \nYou may get inspiration from the default actions in `general.py`.\n\nYou may also have a look into the [snippets](https://gitlab.dlr.de/ioproc/ioproc/-/snippets) section where several basic `ioproc` functionalities are described:\n- [Set up your first workflow](https://gitlab.dlr.de/ioproc/ioproc/-/snippets/155)\n- [Define your first action](https://gitlab.dlr.de/ioproc/ioproc/-/snippets/156)\n- [Make use of checkpoints](https://gitlab.dlr.de/ioproc/ioproc/-/snippets/157)\n- [Define an action making use of the ioproc datamanger](https://gitlab.dlr.de/ioproc/ioproc/-/snippets/158)\n- [Add additional yaml files to your workflow](https://gitlab.dlr.de/ioproc/ioproc/-/snippets/159)\n- [Define global parameters](https://gitlab.dlr.de/ioproc/ioproc/-/snippets/163)\n- [Starting ioproc workflow via command line with additional input parameters](https://gitlab.dlr.de/ioproc/ioproc/-/snippets/168) \n\n## default actions provided by ioProc\n\n### `readExcel`\nThis function is used to parse Excel files and storing it in the Data manager.\n\n```python\n@action(\'general\')\ndef parse_excel(dmgr, config, params):\n    \'\'\'\n    Parses given `excelFile` for specified `excelSheets` as dataframe object and stores it in the datamanager by the \n    key specified in `write_to_dmgr`.\n    `excelHeader` can be set to `True` or `False`.\n    \n    The action may be specified in the user.yaml as follows:\n    - action:\n        project: general\n        call: parse_excel\n        data:\n            read_from_dmgr: null\n            write_to_dmgr: parsedData\n        args:  \n            excelFile: spreadsheet.xlsx\n            excelSheet: sheet1\n            excelHeader: True\n    \'\'\'\n\n    args = params[\'args\']\n    file = get_field(args, \'excelFile\')\n    excel_sheet = get_excel_sheet(args)\n    header = get_header(get_field(args, \'excelHeader\'))\n    parsed_excel = pd.read_excel(io=file, sheet_name=excel_sheet, header=header)\n\n    with dmgr.overwrite:\n        dmgr[params[\'data\'][\'write_to_dmgr\']] = parsed_excel\n```\n\n### `checkpoint`\nCheckpoints save the current state and content of the data manger to disk in HDF5 format. The workflow can be resumed at any time from previously created checkpoints.\n\n```python\n@action(\'general\')\ndef checkpoint(dmgr, config, params):\n    \'\'\'\n    creates a checkpoint file in the current working directory with name\n    Cache_TAG while TAG is supplied by the action config.\n\n    :param tag: the tag for this checkpoint, this can never be "start"\n    \'\'\'\n    assert params[\'tag\'] != \'start\', \'checkpoints can not be named start\'\n    dmgr.toCache(params[\'tag\'])\n    mainlogger.info(\'set checkpoint "{}"\'.format(params[\'tag\']))\n```\n\n### `printData`\nThis action prints all data stored in the data manager to the console. It can therefore be used for conveniently debugging a workflow.\n\n```python\n@action(\'general\')\ndef printData(dmgr, config, params):\n    \'\'\'\n    simple debugging printing function. Prints all data in the data manager.\n\n    Does not have any parameters.\n    \'\'\'\n    for k, v in dmgr.items():\n        mainlogger.info(k+\' = \\n\'+str(v))\n```\n',
    'author': 'Felix Nitsch, Benjamin Fuchs, Judith Riehm, Jan Buschmann',
    'author_email': 'felix.nitsch@dlr.de, benjamin.fuchs@dlr.de, judith.riehm@dlr.de, jan.buschmann@dlr.de',
    'maintainer': 'Felix Nitsch, Benjamin Fuchs, Jan Buschmann',
    'maintainer_email': 'ioproc@dlr.de',
    'url': 'https://gitlab.com/dlr-ve/ioproc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
