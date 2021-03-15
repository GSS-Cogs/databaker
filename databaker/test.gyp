from pandas import ExcelWriter
xls = pd.ExcelFile(inputfile)
with ExcelWriter("data.xls") as writer:
for sheet in xls.sheet_names:
    pd.read_excel(xls, sheet).to_excel(writer,sheet)
    writer.save()
                    
tableset = XLSTableSet(filename="data.xls")