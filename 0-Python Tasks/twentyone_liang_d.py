def twentyone():
    str = input()
    ret = True
    for c in str.lower():
        if c not in '0123456789abcdef':
            ret = False
    print(int(str, 16))

twentyone()
exit()