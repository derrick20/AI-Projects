#!/usr/bin/python3

def one_a():
    x = int(input())
    y = int(input())
    print(x + y)


def one_b():
    list = [int(x) for x in input().split()]
    print(sum(list))

def one_c():
    list = [int(x) for x in input().split() if (int(x) % 3 == 0)]
    print(list)


one_a()
one_b()
one_c()
exit()