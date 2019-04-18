def eighteen():
    str = input()
    ret = ''
    for c in str:
        if c not in ret:
            ret += c
    print(ret)

eighteen()
exit()