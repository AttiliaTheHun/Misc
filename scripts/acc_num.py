# Command-line utility to compute account numbers according to the modulo-11 norm.
# The norm de facto says the weighted sum of the digits of both the prefix and the
# account number must give zero remainder after division by 11.
# Thus if this script answers with 0 for the number you put in, it is an eligible account number.
# An eligible prefix must also be under 7 characters long.

import sys

weights = [1, 2, 4, 8, 5, 10, 9, 7, 3, 6]

def compute_modulo(str):
    if len(str) > len(weights):
        return -1
    _sum = 0
    i = 0;
    for c in reversed(str):
        _sum +=int(c)*weights[i]
        i += 1
    return _sum % 11

def main():
    if len(sys.argv) > 1:
        mod = compute_modulo(sys.argv[1])
        if mod == -1:
            print("number too long")
        else:
            print(mod)
        exit()
    while True:
        num = input("> ")
        if mod == -1:
            print("number too long")
        else:
            mod = compute_modulo(num)
        print(mod)

main()
