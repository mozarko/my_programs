a1 = int(input())
a2 = int(input())
a3 = int(input())
a4 = int(input())

numb = [a1, a2, a3, a4]

for i in range(len(numb) - 1):
    for j in range(len(numb) - i - 1):
        if numb[j] > numb[j + 1]:
            numb[j], numb[j + 1] = numb[j + 1], numb[j]
print(numb[0])
