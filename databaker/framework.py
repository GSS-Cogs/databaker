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

from pathlib import PosixPath

# core classes and functionality
from databaker.jupybakeutils import HDim, HDimConst, ConversionSegment, Ldatetimeunitloose, Ldatetimeunitforce, pdguessforceTIMEUNIT
from databaker.jupybakecsv import writetechnicalCSV, readtechnicalCSV
from databaker.jupybakehtml import savepreviewhtml

from databaker.loaders.xlsx import XLSXTableSet
from databaker.loaders.xls import XLSTableSet
from pandas import ExcelWriter

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

            # Explanation - delete this before you push final please -mike-
            # We're reading the input file object here (our use case) but we need
            # to also support reading a file path
            # logic will be something like "if is_file_object" (the below line) else: 
            # ....something similar to what you had before. 

            df_dict = pd.read_excel(input_file_obj, engine="odf", sheet_name=None)

            # Explanation - delete this before you push final please -mike-
            # so we're actually "saving" to an in-memory BytesIO object rather than
            # a concrete file, this gets us around saving things to disk
            # A BytesIO is just a thing of bytes, and has a read() method (so will satisfy
            # the handling of file_objects in the table loader later)
            # NOTE - we'll always nee to also write TO bytes regardless of if it came in 
            # as filepath or file object

            # had to install xlsxwriter, not sure if thats necessary, have a play
            w = pd.ExcelWriter(BytesIO(), engine='xlsxwriter') 
            for sheet_name in df_dict:
                df_dict[sheet_name].to_excel(w, sheet_name=sheet_name)
            w.save()
            tableset = XLSXTableSet(fileobj=w.book.filename)

    except Exception as err:
        raise err

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
