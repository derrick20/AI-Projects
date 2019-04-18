def five():
    a, b, c = [float(x) for x in input().split()]
    if a + b <= c  or a + c <= b or b + c <= a:
        print('Degenerate Triangle')
    else:
        s = 0.5*(a + b + c)
        print((s*(s-a)*(s-b)*(s-c))**0.5)

five()
exit()