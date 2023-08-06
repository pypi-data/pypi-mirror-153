[![PyPI version](https://badge.fury.io/py/ioproc.svg)](https://badge.fury.io/py/ioproc)
[![PyPI license](https://img.shields.io/pypi/l/ioproc.svg)](https://badge.fury.io/py/ioproc)
[![pipeline status](https://gitlab.dlr.de/ioproc/ioproc/badges/development/pipeline.svg)](https://gitlab.dlr.de/ioproc/ioproc/-/commits/development)
[![coverage report](https://gitlab.dlr.de/ioproc/ioproc/badges/development/coverage.svg)](https://gitlab.dlr.de/ioproc/ioproc/-/commits/development) 

# The ioProc workflow manager
`ioproc` is a light-weight workflow manager for Python ensuring robust, scalable and reproducible data pipelines. The tool is developed at the German Aerospace Center (DLR) for and in the scientific context of energy systems analysis, however, it is widely applicable in other scientific fields.

## how-to install
Setup a new Python environment and install ioProc using 

    pip install ioproc   

## how-to configure

Configure your pipeline in the `user.yaml`. The `workflow` is defined by a list of actions. These must
contain the fields `project`, `call` and `data` (with sub fields `read_from_dmgr`, and `write_to_dmgr`). The user
may specify additional fields for each action under the optional key `args`.  
You may get inspiration from the default actions in `general.py`.

You may also have a look into the [snippets](https://gitlab.dlr.de/ioproc/ioproc/-/snippets) section where several basic `ioproc` functionalities are described:
- [Set up your first workflow](https://gitlab.dlr.de/ioproc/ioproc/-/snippets/155)
- [Define your first action](https://gitlab.dlr.de/ioproc/ioproc/-/snippets/156)
- [Make use of checkpoints](https://gitlab.dlr.de/ioproc/ioproc/-/snippets/157)
- [Define an action making use of the ioproc datamanger](https://gitlab.dlr.de/ioproc/ioproc/-/snippets/158)
- [Add additional yaml files to your workflow](https://gitlab.dlr.de/ioproc/ioproc/-/snippets/159)
- [Define global parameters](https://gitlab.dlr.de/ioproc/ioproc/-/snippets/163)
- [Starting ioproc workflow via command line with additional input parameters](https://gitlab.dlr.de/ioproc/ioproc/-/snippets/168) 

## default actions provided by ioProc

### `readExcel`
This function is used to parse Excel files and storing it in the Data manager.

```python
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
```

### `checkpoint`
Checkpoints save the current state and content of the data manger to disk in HDF5 format. The workflow can be resumed at any time from previously created checkpoints.

```python
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
```

### `printData`
This action prints all data stored in the data manager to the console. It can therefore be used for conveniently debugging a workflow.

```python
@action('general')
def printData(dmgr, config, params):
    '''
    simple debugging printing function. Prints all data in the data manager.

    Does not have any parameters.
    '''
    for k, v in dmgr.items():
        mainlogger.info(k+' = \n'+str(v))
```
