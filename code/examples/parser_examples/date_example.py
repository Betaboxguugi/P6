import arpeggio as apeg

"""
Some notes on the Gregorian calender

01 January - 31 days
02 February - 28 days; 29 days in Leap Years
03 March - 31 days
04 April - 30 days
05 May - 31 days
06 June - 30 days
07 July - 31 days
08 August - 31 days
09 September - 30 days
10 October - 31 days
11 November - 30 days
12 December - 31 days

30 days 4, 6, 9, 11
31 days 1, 3, 5, 7, 8, 10, 12
February 2

1 If the year is evenly divisible by 4, go to step 2. Otherwise, go to step 5.
2 If the year is evenly divisible by 100, go to step 3. Otherwise, go to step 4.
3 If the year is evenly divisible by 400, go to step 4. Otherwise, go to step 5.
4 The year is a leap year (it has 366 days).
5 The year is not a leap year (it has 365 days).
"""


def day31(): return apeg.RegExMatch(r'0[1-9]|1[0-9]|2[0-9]|3[0-1]')  # We use regular expressions to define what is
                                                                     # legal in a string. r'' is a RE in Python


def day30(): return apeg.RegExMatch(r'0[1-9]|1[0-9]|2[0-9]|30')


def day_feb(): return apeg.RegExMatch(r'0[1-9]|1[0-9]|2[0-8]')


def day_feb_leap(): return apeg.RegExMatch(r'0[1-9]|1[0-9]|2[0-9]')


def month31(): return apeg.RegExMatch(r'0(1|3|5|7|8)|1(0|2)'), "-", day31  # We can match tuples too


def month30(): return apeg.RegExMatch(r'0(4|6|9)|11'), "-", day30  # as well as strings like "-"


def month_feb(): return apeg.RegExMatch(r'02'), "-", day_feb


def month_feb_leap(): return apeg.RegExMatch(r'02'), "-", day_feb_leap


def year(): return apeg.RegExMatch(r'[0-9][0-9][0-9][0-9]')


def date(): return year, "-", apeg.OrderedChoice([month31, month30, month_feb]), apeg.EOF  # This is the root rule
                                                                                           # you can tell since
                                                                                           # it has End Of File


def date_leap(): return year, "-", apeg.OrderedChoice([month31, month30, month_feb_leap]), apeg.EOF

# these strings are in the language
input_good = ["2016-03-15", "2016-02-28", "2016-02-29", "2016-01-31", "2016-04-30", "2016-11-30", "2016-12-31",
              "2016-11-29", "2016-12-30", "0001-01-01", "0000-01-01", "1111-11-11", "9998-12-31", "9999-01-01",
              "2020-02-29", "2000-02-29", "1600-02-29", "0400-02-29", "0800-02-29"]

# these are not and will raise an error and halt the program
input_bad = ["2016-04-31", "2016-01-32", "2016-02-30", "2016-00-01", "2016-13-01", "10000-01-01", "001-01-01",
             "2016-01-00", "2015-02-29", "0000-001-01", "0000-01-001", "0000.01.01", "0000/01/01"]
# bad_string = "2016-01-00"
parser = apeg.ParserPython(date)  # We generate a parser using the syntax we defined and enable debugging
parser_leap = apeg.ParserPython(date_leap)  # We actually make 2 parsers
for input_string in input_good:
    year = int(input_string.split("-").pop(0))
    if year % 4 == 0:  # Ifs to catch leap years
        if year % 100 == 0:
            if year % 400 == 0:
                parse_tree = parser_leap.parse(input_string)
                print(parse_tree)

            else:
                parse_tree = parser.parse(input_string)
                print(parse_tree)
        else:
            parse_tree = parser_leap.parse(input_string)
            print(parse_tree)
    else:
        parse_tree = parser.parse(input_string)
        print(parse_tree)

# parse_tree = parser.parse(bad_string)  # I made this to test bad strings, it's not automatic because errors
