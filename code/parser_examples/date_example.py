import arpeggio as apeg

"""
January - 31 days
February - 28 days; 29 days in Leap Years
March - 31 days
April - 30 days
May - 31 days
June - 30 days
July - 31 days
August - 31 days
September - 30 days
October - 31 days
November - 30 days
December - 31 days"""


def day31(): return apeg.RegExMatch(r'0[1-9]|1[0-9]|2[0-9]|3[0-1]')


def day30(): return apeg.RegExMatch(r'0[1-9]|1[0-9]|2[0-9]|30')


def day_feb(): return apeg.RegExMatch(r'0[1-9]|1[0-9]|2[0-8]')


def day_feb_leap(): return apeg.RegExMatch(r'0[1-9]|1[0-9]|2[0-9]')



