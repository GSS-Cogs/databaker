import pandas as pd
from pandas import ExcelWriter
from databaker.loaders.xlsx import XLSXTableSet
from databaker.loaders.xls import XLSTableSet

xls = pd.ExcelFile("/Users/charlesrendle/databaker-docker/xlrd-work/manual-merge/databaker/features/fixtures/bulletindataset2v2 copy.xlsx")
with ExcelWriter("data.xls") as writer:
    for sheet in xls.sheet_names:
        pd.read_excel(xls, sheet).to_excel(writer,sheet)
        writer.save()
                        
tableset = XLSTableSet(filename="data.xls")