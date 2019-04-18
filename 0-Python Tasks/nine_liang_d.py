def nine():
    list = [int(x) for x in input().split()]
    x1 = list[0] # first value
    d = list[1] - list[0] # supposed commond difference
    ret = True

    if x1 not in list[1:]: # this is just checking if the sequence has common differences
        for i in range(2, len(list)):
            if list[i] - list[i - 1] != d:
                ret = False
    else: # there is at least one cycle
        x2_i = list[1:].index(x1)  # second incidence location, since at least one cycle
        m = x2_i + 1 # cycle length can be determined (difference between second and first index, plus one since sliced
        if d >= 0:
            a = min(list)
        else: # might be a decreasing sequence, in which case the max is the a value
            a = max(list)
        i1 = list.index(a)
        for i in range(len(list)):
            if list[i] != a + d * ((i - i1) % m): # fails to satisfy the requirements for cyclicity
                ret = False
    print(ret)

nine()
exit()