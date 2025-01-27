n = int(input())

if n == 1:
    print(n)

f1 = 0
f2 = 1
if n > 1:
    for i in range(n):
        f1, f2 = f2, f1 + f2
        print(f1, end=' ')
