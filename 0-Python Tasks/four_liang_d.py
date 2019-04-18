def is_prime(n):
    ret = False if n < 2 else True
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            ret = False
    return ret

def four_a(n):
    print(is_prime(n))

def four_b(a, b):
    list = []
    for i in range(a+1, b):
        if is_prime(i):
            list.append(i)
    print(list)

def four_c():
    list = [int(x) for x in input().split()]
    if len(list) == 1:
        four_a(list[0])
    else:
        four_b(list[0], list[1])

n = int(input())
four_a(n)

a, b = [int(x) for x in input().split()]
four_b(a, b)

four_c()
exit()