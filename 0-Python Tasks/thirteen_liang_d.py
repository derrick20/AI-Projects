def thirteen_a():
    str = input()
    dict = {}
    for c in str:
        if c in dict:
            dict[c]+= 1
        else:
            dict[c] = 1
    char = max(dict, key = dict.get)
    print(char)

def thirteen_b():
    str = input()
    dict = {}
    for c in str:
        if c in dict:
            dict[c] += 1
        else:
            dict[c] = 1
    max_value = max(dict.values())
    list = []
    for key in dict.keys():
        if dict[key] == max_value:
            list.append(key)
    print(list)

thirteen_a()
thirteen_b()
exit()