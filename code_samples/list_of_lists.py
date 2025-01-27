n = int(input())

lists = [[] for _ in range(n)]

for i in range(n):
    lists[i] = input()

k = int(input()) - 1
for i in range(n):
    if k >= len(lists[i]):
        continue
    print(lists[i][k], end='')
