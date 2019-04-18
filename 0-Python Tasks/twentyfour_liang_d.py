def twentyfour():
    list = input().split()
    key = list[0]
    sub = list[1]
    ret = ''
    for c in ' '.join(list[2:]):
        if c == key:
            ret += sub
        else:
            ret += c
    print(ret)

twentyfour()
exit()