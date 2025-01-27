a = int(input())
b = int(input())

temp = 0
total = 0
max_number = 0
for i in range(a, b + 1):
    for j in range(1, b + 1):
        if i % j == 0:
            temp += j
    if total <= temp:
        total = temp
        max_number = i
    temp = 0
print(max_number, total)

