import sys


MAJOR = sys.version_info[0] 


if MAJOR == 3:
    cmp = lambda a, b: (a > b) - (a < b)  # pragma: no cover
else:  # hopefully MAJOR == 2
    cmp = cmp  # pragma: no cover
