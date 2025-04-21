list = [int(i) for i in input().split()]

i = 0
j = 1
count = 1
while j < len(list):
    if list[j] != list[i]:
        count += 1
    i += 1
    j += 1
print(count)
