def three():
    str = input()
    ret = ''
    for i in range(len(str)):
        if i % 2 == 0:
            ret += str[i]
    print(ret)

three()
exit()