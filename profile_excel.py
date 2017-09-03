
# Imports from the standard Python 2.7 library
import getopt
import sys

# xlrd, see http://www.python-excel.org and https://pypi.python.org/pypi/xlrd
# developed with version 0.9.3
from xlrd import open_workbook

# Local import - tablestat.py defines class TableStat etc.
import tablestat 

'''
Script to profile the values in sheets within an Excel file (xls or xlsx).
'''
 
def profile_excel(header_skip, table, unique_max, file_name, sheet_index):
    '''
    Reads a XLS file using xlrd
    Uses on-demand features to reduce memory requirements.
    TODO: Send date-time values as type datetime.datetime (not float)
    '''
    ts = None
    # detect failure to do anything
    found_sheet = False
    with open_workbook(file_name, on_demand=True) as wb_obj:
        sheet_names = [ n for n in wb_obj.sheet_names() ]
        # print("Sheet names: " + ",".join(sheet_names))
        for idx in xrange(len(sheet_names)):
            if sheet_index is not None and sheet_index != idx:
                continue
            s = wb_obj.sheet_by_name(sheet_names[idx])
            column_names = []
            for rownum in range(s.nrows):
                # get the row's values as a regular list
                row = [ s.cell(rownum,col).value for col in range(s.ncols) ]
                # skip header rows as directed, possibly zero
                if rownum < header_skip:
                    # gather header contents to use as cell names
                    # First ensure list is the right length
                    while len(column_names) < len(row):
                        column_names.append("")
                    column_names = [ column_names[i] + str(row[i]) for i in xrange(len(row)) ]
                    # detect the last header row           
                    if rownum + 1 == header_skip:
                        # instantiate the stat collector
                        ts = tablestat.TableStat(unique_max, column_names)
                else:
                    # special case for header-free inputs
                    if ts is None and header_skip == 0:
                        ts = tablestat.TableStat(unique_max, [])
                    # this is a data row (not a header), analyze it
                    ts.analyze_row(row)
            # for all rows
            # Free some memory
            s = None
            wb_obj.unload_sheet(sheet_names[idx])
            # print report for this sheet
            if table: 
                # emit header when the first sheet is found (a bit of a hack)
                if not found_sheet: ts.print_report_thead("Sheet name,Sheet index,")
                ts.print_report_tbody("%s,%d," % (sheet_names[idx], idx))
            else: 
                print ("---Begin sheet: '%s' (index %d)---" % (sheet_names[idx], idx))
                ts.print_report()
                print ("---End sheet: '%s' (index %d)---" % (sheet_names[idx], idx))
            # If we got here, we found a sheet.
            found_sheet = True
        # for all sheets
    # with
    # warn on bad arguments
    if not found_sheet:
        print("Failed to find sheet at index %d" % sheet_index)
        
def usage():
    '''
    Prints a usage message and exits.
    '''
    print('profile_excel.py [options] file.xls | file.xlsx')
    print('Options:')
    print('   -h header row skip count (default 1)')
    print('   -s sheet-index (default all)')
    print('   -t tabular format report (default no)')
    print('   -u unique-limit (default 20)')
    sys.exit()

def main(args):
    '''
    Parses command-line arguments and profiles the named file.
    '''
    try:
        opts, args = getopt.getopt(args, "h:s:tu:")
    except getopt.GetoptError:
        usage()
    # default values
    hskip = 1
    table = False
    sheetidx = None
    umax = 20
    for opt, optarg in opts:
        if opt in ("-h"):
            hskip = int(optarg)
        elif opt in ("-s"):
            sheetidx = int(optarg)
        elif opt in ("-t"):
            table = True  
        elif opt in ("-u"):
            umax = int(optarg)
        else:
            usage()
    if len(args) != 1:
        usage()
    profile_excel(hskip, table, umax, args[0], sheetidx)

# Pass all params after program name to our main
if __name__ == "__main__":
    main(sys.argv[1:])
            


