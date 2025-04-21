import random

length = int(input())  # длина пароля


def func(n):
    pasw = ''
    for _ in range(n):
        r1 = random.randint(65, 90)
        r2 = random.randint(97, 122)
        list = [r1, r2]
        r3 = random.randint(0, 1)
        pasw += chr(list[r3])
    return pasw


print(func(length))
