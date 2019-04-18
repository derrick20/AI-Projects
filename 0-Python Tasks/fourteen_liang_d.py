def fourteen_a():
    print([word for word in input().split() if word[0] in 'aeiou' and word[len(word) - 1] in 'aeiou'])

def fourteen_b():
    list = [word for word in input().split()]
    ret = []
    for word in list:
        count = 0
        for c in word:
            if c in 'aeiou':
                count += 1
        if count >= 3:
            ret.append(word)
    print(ret)

fourteen_a()
fourteen_b()
exit()
