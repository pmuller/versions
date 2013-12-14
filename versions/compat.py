import sys


MAJOR = sys.version_info[0] 


if MAJOR == 3:
    cmp = lambda a, b: (a > b) - (a < b)
else:  # hopefully MAJOR == 2
    cmp = cmp
