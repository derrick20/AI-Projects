# Derrick Liang 2/8/19
# Kim Period 7
import sys, re

#idx = int(sys.argv[1])-31
myRegexList = [
   "/^0$|^10[01]$/", #DONE
   "/^[01]*$/", # DONE
   "/0$/", # DONE
   "/\w*[aeiou]\w*[aeiou]\w*/i", # DONE
   "/^0$|^1[01]*0$/", # done
   "/^[10]*110[10]*$/", # DONE
   "/^.{2,4}$/s", # DONE
   "/^\d{3} *-? *\d\d *-? *\d{4}$/", # WRONG
   "/^.*?d/m", # WRONG
   "/^[10]$|^1[01]*1$|^0[01]*0$/", # DONE probably?

   "/^[ox.]{64}$/i", # shortest
   "/^[ox]*\.[ox]*$/i", # shortest
   "/^(x.*)?\.|\.(.*x)?$/i",  # "/^(\.|x.*\..*)|(\.|.*\..*x)$/i"
   "/^.(..)*$/s", # shortest
   "/^(1[01]|0)([01]{2})*$/", # shortest
   "/\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*/i", # don't think can be improved
   "/^(1?0)*1*$/", # short
   "/^[bc]*[abc][bc]*$/", # short?
   "/^(b|c|a[bc]*a)+$/", # short
   "/^((1[20]*){2}|2[20]*)+$/", # short
   
   r"/\w*(\w)\w*\1\w*/i",
   r"/\w*(\w)(\w*\1){3}\w*/i",
   r"/^((1|0)[10]*\2|[01])$/",
   r"/\b(?=\w*cat)\w{6}\b/i",
   r"/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/i",
   r"/\b(?!\w*cat)\w{6}\b/i",
   r"/\b((\w)(?!\w*\2))+\b/i", # todo
   r"/^(?!\w*10011)[01]*$/",
   r"/\b\w*([aeiou])(?!\1)[aeiou]\w*/i",
   "/^(?!\w*1[01]1)[01]*$/",
   # skip 61-70

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
'''
phosphorescence's
Chancellorsville's
misconstruction's
plainclothesman's
synchronization's
crystallization's
transplantation's
circumscription's
whatchamacallit's
flibbertigibbet's

phosphorescence's 
plainclothesman's 
infrastructure's 
conjunctivitis's 
superstructure's 
newspaperwoman's 
circumscription's 
straightjacketed 
transmigration's 
circumspection's 
flibbertigibbet's 
procrastinator's 
schoolmistresses 
transcontinental 
apprenticeship's 
characteristic's 
'''

str = 'Potato'
regex = "\w*[aeiou]\w*[aeiou]\w*"
#print(re.findall(regex, str, re.MULTILINE))

regexList = [
    r"/^(?=.*(.)(.*\1){3}).{,6}$/m", # WHY DON"T THESE WORK
    r"/^(?=.*a)(?=.*e)(?=.*i)(?=.*o)(?=.*u).{,8}$/im",
    r"/(?=(\b([^aeiou\n]*[aeiou]){5}[^aeiou\n]\b)).{17,}$/im",
    r"/^(?=.*(.)(.)(.)\b)\3\2\1.{6,}$/im",
    r"/(?=.*(.)\1+).{20,}$/m", # requires at least two in a row, should work for general cases
    r"/(?=.*(.)(.*\1){5,})\w{14,}/",
    r"/(?=(.*(.)\2){3})\w{14,}/",
    "",
    "",
    r"/(?!.*(.)(.*\1){2})\w{18,}$/m"
]
#prin
total = 0
for reg in regexList:
   deleted = 0
   for delete in "/ims":
      deleted += reg.count(delete)
   total += len(reg) - deleted
print(total-8) #'''
#print(myRegexList[idx])

#Hint for how to write each RegEx
#Sample answer to check a string is 'a': "/^a$/"
#Sample answer to check each line start with a word character: "/^\\w/m"

'''
X means syntax error
E means script error
T means time out
M means missing
D means no trailing /
O means bad option
I means invalid regular expression
P means shouldn't be doing this
N means internal error
r'\ makes no \\
'''
