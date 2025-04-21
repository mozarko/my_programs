list = []

for el in input().split():
    if list and el in list[-1]:
        list[-1].append(el)
    else:
        list.append([el])

print(list)
