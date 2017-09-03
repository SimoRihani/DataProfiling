import xlrd
import xlwt
from optparse import OptionParser
import datetime

"""
Merges excel files with multiple sheets with identical header lines into
a new excel book with one sheet and only one header line.
The columns are shifted one place to the right to make space for a new column
which is filled with the value of the current sheet.
Requirements:
xlrd
xlwt
Options:
-f the filename of the xls file with multiple sheets with identical header rows
-s The zero-indexed row to start reading data from. Not header-row
-r The zero-indexed headerrow on the first sheet. Used for header on the new single sheet
-o the name of the output (merged) xls file
-d the date format to use on the new excel file on columns with dates. Defaults to DD-MM-YYYY
Usage:
sheet.py -f mydata.xls -s 2 -r 1 -o merged.xls
----
Created by Anders G. Eriksen (@anderseri) 2011
"""

def betweensheets():

    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                  help="Excel file to read", metavar="FILE")

    parser.add_option("-o", "--outputfile", dest="outputfile",
                  help="The name/path of the merged excel file", metavar="OUTPUTFILE", default="out.xls")

    parser.add_option("-s", "--startrow", dest="startrow",type="int",
                  help="Row to start reading data on each sheet", metavar="STARTROW", default=1)

    parser.add_option("-r", "--headerrow", dest="headerrow",type="int",
                  help="The row in sheet one that contains the headers", metavar="HEADERROW", default=0)

    parser.add_option("-d", "--dateformat", dest="dateformat",type="str",
                  help="Date format (defaults to DD-MM-YYYY)", metavar="DATEFORMAT", default="DD-MM-YYYY")

    (options, args) = parser.parse_args()

    book = xlrd.open_workbook(options.filename, formatting_info=True)

    merged_book = xlwt.Workbook()
    ws = merged_book.add_sheet("merged")

    rowcount = 0

    datestyle = xlwt.XFStyle()
    datestyle.num_format_str = options.dateformat

    for sheetx in range(book.nsheets):
        sheet = book.sheet_by_index(sheetx)
        for rx in range(sheet.nrows):

            if rx == options.headerrow and sheetx == 0:
                ws.write(rowcount, 0, "sheetname")
                for cx in range(sheet.ncols):
                    ws.write(rowcount, cx+1, sheet.cell_value(rx, cx))
                rowcount += 1

            if rx > (options.startrow-1):
                ws.write(rowcount, 0, sheet.name)
                for cx in range(sheet.ncols):
                    value = sheet.cell_value(rx, cx)

                    #datetime check lifted from the great Everyblock ebdata excel.py code
                    #http://code.google.com/p/ebcode/

                    if sheet.cell_type(rx, cx) == 3:
                        try:
                            value = datetime.datetime(*xlrd.xldate_as_tuple(value, book.datemode))

                            ws.write(rowcount, cx+1, sheet.cell_value(rx, cx), datestyle)
                        except ValueError:
                            # The datetime module raises ValueError for invalid
                            # dates, like the year 0. Rather than skipping the
                            # value (which would lose data), we just keep it as
                            # a string.
                            pass
                    else:
                        ws.write(rowcount, cx+1, sheet.cell_value(rx, cx))

                rowcount += 1

    merged_book.save(options.outputfile)

if __name__ == '__main__':
    betweensheets()
