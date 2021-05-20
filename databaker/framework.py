import logging
import os, warnings
from io import BytesIO
import messytables
import xypath
import xypath.loader
import databaker.constants
from databaker.constants import *      # also brings in template
import databaker.overrides as overrides       # warning: injects additional class functions into xypath and messytables

import pandas as pd
from pandas import ExcelWriter

from pathlib import PosixPath

# core classes and functionality
from databaker.jupybakeutils import HDim, HDimConst, ConversionSegment, Ldatetimeunitloose, Ldatetimeunitforce, pdguessforceTIMEUNIT
from databaker.jupybakecsv import writetechnicalCSV, readtechnicalCSV
from databaker.jupybakehtml import savepreviewhtml

from databaker.loaders.xlsx import XLSXTableSet
from databaker.loaders.xls import XLSTableSet

def loadxlstabs(input, sheetids="*", verbose=True):

    is_file_object = not isinstance(input, str) and not isinstance(input, PosixPath)
    input_file_name = input.name if is_file_object else input
    input_file_obj = input if is_file_object else None

    if verbose:
        if is_file_object:
            print(f'Loading fileobject {input_file_name} which has size {input_file_obj.__sizeof__()} bytes')
        else:
            print(f'Loading file {input_file_name} which has size {os.path.getsize(input_file_name)} bytes')

    try:
        if str(input_file_name).endswith(".xlsx"):
            tableset = XLSXTableSet(filename=input_file_name, fileobj=input_file_obj)
        elif str(input_file_name).endswith(".xls"):
            tableset = XLSTableSet(filename=input_file_name, fileobj=input_file_obj)
        elif str(input_file_name).endswith(".ods"):
            df_dict = pd.read_excel(input_file_name, engine="odf", sheet_name=None)
            w = pd.ExcelWriter(BytesIO(), engine='xlsxwriter') 
            #for sheet_name in df_dict:
            for key in df_dict.keys():
                df_dict[key].to_excel(w, sheet_name=key, index=False)
                #df_dict[sheet_name].to_excel(w, sheet_name=sheet_name)
            w.save()
            tableset = XLSXTableSet(fileobj=w.book.filename)

    except Exception as err:
        logging.warning(f'Internal table loader failure with exception:\n\n {str(err)}\n\n. '
                        'Falling through to default messytables table loader.')
        tableset = messytables.excel.XLSTableSet(filename=input_file_name, fileobj=input_file_obj)
    
    tabs = list(xypath.loader.get_sheets(tableset, sheetids))
    assert len(tabs) > 0, f'Aborting. Unable to acquire any data tables'
    
    tabnames = [ tab.name  for tab in tabs ]
    if verbose:
        print("Table names: %s" % str(tabnames))
    
    if sheetids != "*":
        if type(sheetids) == str:
            sheetids = [sheetids]
        assert type(sheetids) in [list, tuple], ("What type is this?", type(sheetids))
        for sid in sheetids:
            assert sid in tabnames, (sid, "missing from found tables")
        assert len(sheetids) == len(tabnames), ("Number of selected tables disagree", "len(sheetids) == len(tabnames)", len(sheetids), len(tabnames))
    if len(set(tabnames)) != len(tabnames):
        warnings.warn("Duplicates found in table names list")

    return tabs

DATABAKER_INPUT_FILE = None


def getinputfilename():
    """ Return DATABAKER_INPUT_FILE from os.environ or this module.

    This is so that DATABAKER_INPUT_FILE could be specified in a notebook and
    then overridden by an environment variable if not.

    Use of environment variables is because nbconvert doesn't allow you to
    easily pass arguments to the notebook.

    Use in notebook is along the lines of:

    DATABAKER_INPUT_FILE = 'myfile.xls'
    f = getinputfilename()

    This way, we can set the filename in the notebook, or at the commmand line
    with environment variables.
    """
    try:
        return os.environ['DATABAKER_INPUT_FILE']
    except KeyError as e:
        return DATABAKER_INPUT_FILE
