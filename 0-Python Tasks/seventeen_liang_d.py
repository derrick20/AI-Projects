def seventeen():
    str = input()
    dict = {}
    for c in str:
        if c in dict:
            dict[c] += 1
        else:
            dict[c] = 1
    for c in dict.keys():
        if dict[c] == 1:
            print(c) # assumes there is one in the first place...
            break

seventeen()
exit()