def sixteen():
    str = input()
    max_index = 1
    for i in range(2, len(str)):
        if ord(str[i]) - ord(str[i - 1]) > ord(str[max_index]) - ord(str[max_index - 1]):
            max_index = i
    print(str[max_index - 1] + ', ' + str[max_index])

sixteen()
exit()
