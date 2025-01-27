n = int(input())
k = int(input())
j = 0

for i in range(1, n + 1):
    j = (j + k) % i

print(j + 1)
