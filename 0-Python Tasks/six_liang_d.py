def six():
    str = input()
    ret = ''
    for c in str:
        if c not in ''' ~!@#$%^&*()_+{}|:"<>?`-=[]\;',./''':
            ret += c
    print(ret)

six()
exit()