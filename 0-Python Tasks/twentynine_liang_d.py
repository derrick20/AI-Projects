def twentynine():
    str = input()
    for p in set(perm(str)):
        print(p)

def perm(str): # returns a list of permutations of str
    n = len(str)
    if len(str) == 0: # base case
        return []
    elif len(str) == 1:
        return [str]
    else:
        list = []
        for i in range(len(str)): # fix each
            for p in perm(str[:i] + str[i + 1:]): # so, the char at i has been tossed out and the string
                list.append(str[i] + p)
                # re-concatenated, recursively breaking it down. so this fixes each character
                # in the str at the first position, and appends all permutations of the
                # remaining portion of the string.
        return list

twentynine()
exit()