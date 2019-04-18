def eleven():
    a,b = [int(x) for x in input().split()]
    list = []
    for i in range(a, b + 1):
        list.append(i**2 - 3*i + 2)
    print(list)

eleven()
exit()