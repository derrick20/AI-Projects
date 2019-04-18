def simplify(str):
    ret = ''
    for c in str:
        if c not in ''' ~!@#$%^&*()_+{}|:"<>?`-=[]\;',./''':
            ret += c
    return ret.lower()

def seven():
    str = simplify(input())
    print(True if str == str[::-1] else False)

seven()
exit()