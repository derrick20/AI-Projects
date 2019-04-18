def two():
    n = int(input())
    fib = []
    fib.append(1)
    for i in range(1, n):
        if i <= 3:
            fib.append(i)
        else:
            fib.append(fib[i-1] + fib[i-2])
    print(fib)

two()
exit()