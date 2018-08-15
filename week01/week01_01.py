import sys

string = sys.argv[1]

_sum = 0

for c in string:
    n = int(c)
    _sum += n

print(_sum)
