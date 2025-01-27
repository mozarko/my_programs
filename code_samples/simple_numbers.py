a = int(input())
b = int(input())

for i in range(a, b + 1):
    temp = 0
    for j in range(1, i + 1):
        if i % j == 0:
            temp += 1
    if temp == 2:
        print(i)
