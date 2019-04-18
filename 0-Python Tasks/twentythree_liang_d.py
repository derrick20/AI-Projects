def twentythree():
    str = input()
    s = str[str.index(' ') + 1:]
    key = str[:str.index(' ')]
    l = len(key)
    count = 0
    for i in range(0, len(s) - l + 1):
        if key == s[i:i + l]:
            count += 1
    print(count)

twentythree()
exit()