from math import factorial as fc


def pascal(n):
    pascal = [0] * (n + 1)
    if n == 0:
        pascal = [1]
        return pascal
    if n == 1:
        pascal = [1, 1]
        return pascal
    if n == 2:
        pascal = [1, 2, 1]
        return pascal
    if n > 2:
        pascal[0] = pascal[-1] = 1
        pascal[1] = pascal[-2] = n
        for i in range(2, (n - 1)):
            pascal[i] = int(fc(n) / (fc(i) * fc(n - i)))
        return pascal


n = int(input())

for i in range(n):
    print(*pascal(i))
