def twentyfive():
    str1 = input('First: ')
    str2 = input('Second: ')
    print({char:str1.count(char) for char in set(str1)} == {char:str2.count(char) for char in set(str2)})

twentyfive()
exit()