def thirty():
    L = {}
    str = input()
    L[0] = str[0] # bottom-up base case
    for i in range(1, len(str)): # i represents the last pos of the sequence
        L[i] = '' # have to initialize
        for j in range(i): # j is where we take an LIS from a subproblem
            if ord(str[j]) < ord(str[i]) and len(L[j]) + 1 > len(L[i]): # so it's incr and makes it longer
                L[i] = L[j]
        L[i] += str[i] # append the required final character
    print(max(L.values()))

thirty()
exit()