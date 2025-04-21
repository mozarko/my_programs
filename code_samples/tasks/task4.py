def fact(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * fact(n - 1)


try:
    n = int(input())
except ValueError:
    print("Natural number was expected", end="")
    exit(1)

if n < 0:
    print("Natural number was expected", end="")
    exit(1)

if n == 0:
    print("1", end="")
    exit(0)

for i in range(0, n):
    for k in range(0, i + 1):
        print(int(fact(i) / (fact(k) * fact(i - k))), end="")
        if (k != i):
            print(" ", end="")
    if (i != n - 1):
        print()

exit(0)
