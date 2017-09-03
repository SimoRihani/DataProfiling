'''
Created on Aug 24, 2017
@author: Simo Rihani
'''

# future must be first
from __future__ import print_function
import datetime

# Simple enum
# http://stackoverflow.com/questions/36932/how-can-i-represent-an-enum-in-python
#class Enum(set):
#    def __getattr__(self, name):
#        if name in self:
#            return name
#        raise AttributeError
# This avoids repeating string constants
#Datatype = Enum(["charstring", "digitstring", "number", "date", "mixed", "unknown"])
# Constant values for speedy comparisons.
# A pseudo enum is clearer but runs lots of code.
datatype_unknown = -1
datatype_charstring = 0
datatype_digitstring = 1
datatype_number = 2
datatype_date = 3
datatype_mixed = 4

def get_datatype_name(d):
    '''
    Translates integers to strings for reporting.
    '''
    if d == datatype_charstring:     return "Charstring"
    elif d == datatype_digitstring:  return "Digitstring"
    elif d == datatype_number:       return "Number"
    elif d == datatype_date:         return "Date"
    elif d == datatype_mixed:        return "Mixed"
    else:                            return "Unknown"

# Inherits only from object
class TableStat(object):
    '''
    Provides methods to gather and report descriptive statistics on a
    table of strings; for example, useful to profile a CSV file.
    Also handles integer, float and None values.

    Designed to be instantiated with a list of column names, but can
    also be created with an empty list; it will then self-assign names.

    Combines count of "None" values with count of empty string values.

    This code has been tuned for performance to handle large inputs.
    On a 3.1GHz win7 PC this requires about 1 min / 1 million rows,
    depending on the number of columns of course.

    Useful attributes:
        unique_max (integer)
        row_count (integer)
        stats (list of ColumnStat objects)

    Profiled with "-m cProfile" arguments to python
    '''

    def __init__(self, unique_max_count, column_list):
        '''
        Constructor accepts an ORDERED list of column names.
        If the list is empty, assigns names as it does.
        '''
        # validate the input arguments
        if not isinstance(unique_max_count, int):
            raise Exception("Expected int but received %s" % type(unique_max_count))
        if not isinstance(column_list, list):
            raise Exception("Expected list but received %s" % type(column_list))
        # Keep the limit on unique values
        self.unique_max = unique_max_count
        # Number of rows seen
        self.row_count = 0
        # List of stat-collection objects, one per column
        self.stats = [ ColumnStat(i, column_list[i], self.unique_max) for i in xrange(len(column_list)) ]

    def analyze_row(self, data_list):
        '''
        Gathers statistics from the ORDERED list of data, which must match
        match the order and count of columns given to constructor.
        '''
        self.row_count += 1
        # compute length once, not repeatedly
        datalen = len(data_list)
        # Extend for wider-than-expected rows; nothing to do for narrow rows.
        if len(self.stats) < datalen:
            # Don't warn if column names began as an empty list
            if  len(self.stats) > 0:
                print("Warning: input row %d has %d columns but expected %d" % (self.row_count, datalen, len(self.stats)))
            while len(self.stats) < datalen:
                # Grow the list of column stat objects to allow
                # extra columns, or starting with no columns defined
                self.stats.append(ColumnStat(len(self.stats), None, self.unique_max))
        # Analyze each field in this row
        for i in xrange(datalen):
            self.stats[i].analyze_value(data_list[i])

    def print_report(self):
        '''
        Prints report on all columns to stdout, one result per line.
        This is convenient for humans.
        '''
        print("Row count = %d" % self.row_count)
        print("Note: unique value limit = %d" % self.unique_max)
        for i in xrange(len(self.stats)):
            self.stats[i].print_report()

    def print_report_thead(self, prefix):
        '''
        Prints header for column-oriented report.
        Prefix is used for additional column heads.
        '''
        self.stats[0].print_report_head(prefix)

    def print_report_tbody(self, prefix):
        '''
        Prints body of column-oriented report.
        Prefix is used for additional data columns.
        '''
        for i in xrange(len(self.stats)):
            self.stats[i].print_report_row(prefix)

# Inherits only from object
class ColumnStat(object):
    '''
    Gathers and reports descriptive statistics on a
    collection of values, such as a single column in a table.
    Constructor takes index, name, unique_max limit.

    Useful attributes:
        name (string)
        datatype (inferred)
        empty (count of empty values)
        nonempty (count of non-empty values)
        values (set of unique values, up to limit)
		freqs (dict of unique values and their frequencies)
        minval, maxval (minimum and maximum numeric values)
        minlen, maxlen (minimum and maximum string lengths)
    '''

    def __init__(self, col_index, col_name, unique_max):
        # Keep the index & name
        self.index = col_index
        self.name = col_name
        # Limit set size to this maximum
        self.unique_max = unique_max
        # Datatype is inferred for strings
        self.datatype = datatype_unknown
        # Number of None, empty string or all-whitespace entries
        self.empty = 0
        # Number of non-empty entries
        self.nonempty = 0
        # constants used as sentinels
        self.minsentinel = 999999999
        self.maxsentinel = -1
        # min and max lengths for strings
        self.minlen = self.minsentinel
        self.maxlen = self.maxsentinel
        # min and max values for numbers
        self.minval = self.minsentinel
        self.maxval = self.maxsentinel
        # min and max values for dates
        self.mindate = None
        self.maxdate = None
        # Unique value frequencies (size is limited)
        self.freqs = {}
        # set when freqs grows too long
        self.freqsfull = False

    def analyze_value(self, value):
        '''
        Analyzes a new value (i.e., new row) for the column.

        This is the critical method for performance tuning.
        '''
        # Track unique values/frequencies, limited by unique_max.
        if not self.freqsfull:
            if len(self.freqs) < self.unique_max:
                # use get method's default value feature
                self.freqs[value] = self.freqs.get(value, 0) + 1
            else:
                # set flag in hope that boolean test is very fast
                self.freqsfull = True

        # Test for type
        if value is None:
            # This is not really expected, but don't blow up.
            self.empty += 1
        # this is a python 2.x solution; doesn't work in 3
        elif isinstance(value, basestring):
            # It has some kind of string.
            if value == "" or value.isspace():
                self.empty += 1
                # Don't infer type based on a zero-length string.
                # TODO: possibly turn off digitstring on non-zero whitespace?
            else:
                self.nonempty += 1
                # infer type of data within the string
                if value.isdigit():
                    # this value is only numbers
                    if self.datatype == datatype_digitstring:
                        # this is the most common case, no need to look further
                        pass
                    elif self.datatype == datatype_unknown:
                        # first sighting
                        self.datatype = datatype_digitstring
                    elif self.datatype != datatype_charstring and self.datatype != datatype_digitstring:
                        # previously had non-string value, so mark as mixed
                        self.datatype = datatype_mixed
                else:
                    # not digits
                    if self.datatype == datatype_charstring:
                        # this is the most common case, no need to look further
                        pass
                    elif self.datatype == datatype_unknown or self.datatype == datatype_digitstring:
                        # first sighting, or first presence of chars
                        self.datatype = datatype_charstring
                    elif self.datatype != datatype_charstring:
                        # previously had non-string type
                        self.datatype = datatype_mixed
                # done with type
            # track min/max length of the string
            # calculate length once, not 2+ times
            strlen = len(value)
            if strlen < self.minlen: self.minlen = strlen
            if strlen > self.maxlen: self.maxlen = strlen

        elif isinstance(value, int) or isinstance(value, long) or isinstance(value, float):
            # It's a proper number.
            self.nonempty += 1
            # Note type
            if self.datatype == datatype_unknown: self.datatype = datatype_number
            elif self.datatype != datatype_number: self.datatype = datatype_mixed
            # Store min/max numeric values
            if value < self.minval: self.minval = value
            if value > self.maxval: self.maxval = value

        elif isinstance(value, datetime.datetime):
            # It's a date-time value; first seen from XLSX via openpyxl
            self.nonempty += 1
            # Note type
            if self.datatype == datatype_unknown: self.datatype = datatype_date
            elif self.datatype != datatype_date: self.datatype = datatype_mixed
            # Store min/max date values
            if self.mindate is None or value < self.mindate: self.mindate = value
            if self.maxdate is None or value > self.maxdate: self.maxdate = value

        else:
            # Tabular data should not have non-scalar values like list, etc.
            raise Exception("Cannot profile type " + str(type(value)))

            # not a string

    def print_report(self):
        '''
        Prints field report to stdout, one result per line.
        '''
        print("Column '%s' (index %d)" % (self.name, self.index))
        print("\tData type      = %s" % get_datatype_name(self.datatype))
        print("\tEmpty count    = %d" % self.empty)
        print("\tNonempty count = %d" % self.nonempty)
        print("\tDensity        = %f" % self.get_density())
        if self.datatype == datatype_charstring or self.datatype == datatype_digitstring:
            print("\tMax length str = %s" % self.maxlen)
            print("\tMin length str = %s" % self.minlen)
        if self.datatype == datatype_number:
            print("\tMax number     = %s" % self.maxval)
            print("\tMin number     = %s" % self.minval)
        if self.datatype == datatype_date:
            print("\tMax date       = %s" % self.maxdate)
            print("\tMin date       = %s" % self.mindate)
        # Don't just echo the max value count when it's exceeded
        if len(self.freqs) < self.unique_max:
            print("\tUnique count   = %d" % len(self.freqs))
            # emit dictionary contents sorted by key
            print("\tUnique values  = %s" % "{" + ", ".join("%r: %r" % (key, self.freqs[key]) for key in sorted(self.freqs)) + "}")
        else:
            print("\tUnique count   > %d" % self.unique_max);

    def get_density(self):
        return (self.nonempty / float(self.empty + self.nonempty))

    def print_report_head(self, prefix):
        '''
        Prints the column heads for a tabular report to stdout.
        Use in conjunction with print_report_row.
        Optionally adds a prefix, which supports sheet name and index.
        '''
        print(prefix + "Column name,Column index,Data type,Empty count,Nonempty count,Density,"
              + "Max length str,Min length str,Max number,Min number,Max date,Min date,"
              + "Unique count,Unique values")

    def print_report_row(self, prefix):
        '''
        Prints field report to stdout, one result per column.
        Optionally adds a prefix, which supports sheet name and index.
        '''
        # Avoid a hopelessly wide line.
        if len(self.freqs) < self.unique_max:
            myuniques = str(len(self.freqs))
            # emit dictionary contents sorted by key
            myfreqs = "{" + ", ".join("%r: %r" % (key, self.freqs[key]) for key in sorted(self.freqs)) + "}"
        else:
            myuniques = "> " + str(self.unique_max)
            myfreqs = "Unknown"
        print(prefix
              + "%s," % self.name
              + "%d," % self.index
              + "%s," % get_datatype_name(self.datatype)
              + "%d," % self.empty
              + "%d," % self.nonempty
              + "%f," % self.get_density()
              + "%s," % (self.maxlen if self.maxlen != self.maxsentinel else None) # emit as string to allow None
              + "%s," % (self.minlen if self.minlen != self.minsentinel else None)
              + "%s," % (self.maxval if self.maxval != self.maxsentinel else None)
              + "%s," % (self.minval if self.minval != self.minsentinel else None)
              + "%s," % self.maxdate
              + "%s," % self.mindate
              + "%s," % myuniques
              + '"%s"' % myfreqs     # surround with quotes
            )


# Basic tests
# TODO: How to generate a date-time value?
if __name__ == "__main__":
    cols = [ "Empties", "Numbers", "Strings", "Digitstring" ]
    ts = TableStat(unique_max_count = 5, column_list = cols)
    ts.analyze_row([None , None, None   , None  ])
    ts.analyze_row(["   ", 1   , "hi"           ])
    ts.analyze_row(["\t" , 2   , "world", "456", "bonus" ])
    ts.analyze_row([None , 3.0 , "bar"  , "789" ])
    ts.analyze_row([None , 4.0 , "bar"  , "012" ])
    print("Generating tall report:")
    ts.print_report()
    print("Generating wide report:")
    ts.print_report_thead("")
    ts.print_report_tbody("")
    # This tests constructor input validation
    # bogus = TableStat("hi")
