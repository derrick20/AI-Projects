import sys, re

file = open("wordsC.txt")#("longwordswithvowels")
dic = ''.join(file.readlines())

# print(max(dic, key=len))

regexList = [
    r"^[^aeiouy\n]w[^aeiouy\n]$",
    r"^((\w)(?!\w*\2)){15,}$",
    r"^(?=(([aeiou])(?!\w*\2)[^aeiou\n]*){5})\w{16,}$"
]

for pattern in regexList:
    if pattern != r"":
        regex = re.compile(pattern, re.M | re.I)
        re_list = [dic[m.start():m.end()] for m in regex.finditer(dic)]
        print(re_list)
