def nineteen():
    str = input()
    ret = True
    for c in str:
        if c not in '0123456789':
            ret = False
    print(ret)

nineteen()
exit()