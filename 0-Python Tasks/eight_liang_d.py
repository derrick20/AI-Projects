def eight():
   str = input()
   count = 0
   for c in str.lower():
      if c in 'aeiou':
         count += 1
   print(count)

eight()
exit