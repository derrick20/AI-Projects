import sys, re

file = open("ghostDictionary.txt")
dic = ''.join(file.readlines())

#import sys
#idx = int(sys.argv[1])-71
regexList = [
    r"/\b(?=(.)+(.*\1){3}).{,6}$/", # 25, perfect
    r"/^((?=.*([aeiou]))(?!.*\1)){5}.{,8}$/m",
    #r"/^(?=.*a)(?=.*e)(?=.*i)(?=.*o).{,4}u.{,4}$/m",
    r"/(?=(\b([^aeiou\n]*[aeiou]){5}[^aeiou\n]\b)).{16,}$/", # 50 bad 5 above
    r"/(?=\b(.)+(\w)(\w)\b)\3\2\1\w{6,}$/", # 33, 11 above
    r"/(?=\(.)+\1{1,})\w{20,}/", # DONE 22 requires at least two in a row, should work for general cases
    r"/(?=(.)+(.*\1){5,})\w{14,}/", # 25  too high
    r"/(?=((.)+\2){3})\w{14,}/", # DONE 22
    r"",
    r"",
    r"/\b(?!(.)+(.*\1){2})\w{18,}\b/" # DONE 28
    
    
    r"/^(?=(.)+(.*\1){3}).{,6}$/m", # 25
    r"/^(?=(.*([aeiou])(?!.*\2)){5}).{,8}$/m", # 35
    r"/^(?=([^aeiou]*[aeiou]){5}[^aeiou]*$).{18,}$/im", # 43, didn't need \n since $ anchors it
    r"/^(.)(.)(.).{2,}\3\2\1$/m", # 22 it's better not to do the reverse thinking way
    r"/(?=(.)+\1).{20,}$/m", # 17 requires at least two in a row, should work for general cases
    #r"/(?=(.)+(.*\1){5})\w*$/m", # 25 6 above
    r"/(.)+(\w*\1){5,}\w*$/m", # 19 yay
    r"/(?=((.)+\2){3})\w{14,}/", # 22
    "",
    "",
    r"/(?!(.)+(.*\1){2})\w{18,}$/m" # 25
]
#print(regexList[idx])

for pattern in regexList:
    if pattern is not r"":
        regex = re.compile(pattern, re.M)
        re_list = [dic[m.start():m.end()] for m in regex.finditer(dic)]
        print (re_list)

#case insensitivity? Contractions? etc.

#Example 1: find words ending with bt
'''
pattern = ".*bt$"  # 
print (re.findall(pattern, dic, re.MULTILINE))

#Example 2: find the longest word
pattern = ".{23,}" #
print (re.findall(pattern, dic, re.MULTILINE))

#Example 3: Find the longest word where no vowel appears more than twice.
pattern = r'^(?!.*([aeiou])(\w*\1){2})\w{19,}'
regex = re.compile(pattern, re.M)
re_list = [dic[m.start():m.end()] for m in regex.finditer(dic)]
print (re_list)

'''