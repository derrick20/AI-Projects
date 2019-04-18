def twentyseven():
    str = input()
    pal = ''
    for pos in range(len(str)):
        i = 0
        while pos - i >= 0 and pos + i <= len(str) - 1 and str[pos - i] == str[pos + i]: # palindrome centered at pos may be extended further
            i += 1
        i -= 1 # the last loop will increase it too far, so decrement
        test = str[pos - i: pos + i + 1] # longest pal at this center
        if len(test) > len(pal):
            pal = test
    print(pal)

twentyseven()
exit()
