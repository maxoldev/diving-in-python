import sys
import operator

a = int(sys.argv[1])
b = int(sys.argv[2])
c = int(sys.argv[3])

D = b ** 2 - 4 * a * c


def find_root(op):
    x = (op(-b, D ** 0.5)) / (2 * a)
    return x


if D > 0:
    print(int(find_root(operator.sub)))
    print(int(find_root(operator.add)))
elif D == 0:
    print(int(find_root(operator.sub)))  # roots are equal
else:
    print("no rational number roots")
