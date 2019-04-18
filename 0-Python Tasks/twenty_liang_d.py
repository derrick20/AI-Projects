def twenty():
    str = input()
    ret = True
    for c in str:
        if c not in '01':
            ret = False
    print(int(str, 2))
    '''value = 0
    current = 0
    if ret:
        for c in str[::-1]:
            value += (2**current) * int(c)
            current += 1''' # unnecessary way

twenty()
exit()