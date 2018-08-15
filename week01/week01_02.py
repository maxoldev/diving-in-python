import sys

string = sys.argv[1]
num_steps = int(string)

num_spaces = 0
num_sharps = 0


def print_line():
    _string = ""
    for _ in range(num_spaces):
        _string += " "

    for _ in range(num_sharps):
        _string += "#"
    print(_string)


for i in range(num_steps):
    num_sharps = i + 1
    num_spaces = num_steps - num_sharps
    print_line()
