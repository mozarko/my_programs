n = int(input())
list = []

for _ in range(n):
    a = int(input())
    list.append(a)


i = 0
sum = 0
list2 = []
while i < n - 1:
    sum = list[i] + list[i + 1]
    list2.append(sum)
    i += 1
print(list2)