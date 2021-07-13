

# Dev notes:
# ----------
# We've experienced issues where excel files converted via libra office can have broken/malformed
# property values. This issues results in a uncaught exception and failed processing.
#
# This "monkey patch" applies to the default messytables table loader (which we fall back on
# upon encountered table loading exceptions) and should allow us to still process spreadsheets when 
# this edge case is encountered.

import functools

from messytables import excel
from messytables.excel import XLSProperties


def bold_wrapper(old_get_bold):
    @functools.wraps(old_get_bold)
    def new_get_bold(self):
        try:
            return old_get_bold(self)
        except:
            return False

    return new_get_bold


XLSProperties.get_bold = bold_wrapper(XLSProperties.get_bold)


def new_xf(self):
    if self.cell.xlrd_cell.xf_index in self.cell.sheet.book.xf_list:
        return self.cell.sheet.book.xf_list[self.cell.xlrd_cell.xf_index]
    else:
        return None


def new_formatting(self):
    if self.xf is not None and self.xf.format_key in self.cell.sheet.book.format_map:
        return self.cell.sheet.book.format_map[self.xf.format_key]
    else:
        return None


def get_formatting_wrapper(old_get_formatting):
    @functools.wraps(old_get_formatting)
    def new_get_formatting(self):
        formatting = self.formatting
        if formatting is None:
            return ''
        else:
            return formatting.format_str
    return new_get_formatting


XLSProperties.get_formatting_string = get_formatting_wrapper(XLSProperties.get_formatting_string)
setattr(XLSProperties, 'xf', property(new_xf))
setattr(XLSProperties, 'formatting', property(new_formatting))