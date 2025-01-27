try:
    n, hours = map(int, input().split())
except ValueError:
    print("n/a", end="")
    exit(1)

lists = []

try:
    for i in range(n):
        lists.append(list(map(int, input().split())))
except ValueError:
    print("n/a", end="")
    exit(1)

count = {}
uniq_list = []
for i in range(n):
    key = lists[i][0]
    if key not in count:
        count[key] = 0
    count[key] += 1

for key, values in count.items():
    if values > 1:
        uniq_list.append(key)

lists.sort(key=lambda x: (x[1], x[2]))

result_list = []
for i in range(n):
    if lists[i][0] in uniq_list:
        result_list.append(lists[i])

for i in range(len(result_list)):
    for j in range(i + 1, len(result_list)):
        if (result_list[i][0] == result_list[j][0]) and (result_list[i][2] + result_list[j][2]) >= hours:
            print(result_list[i][1] + result_list[j][1], end="")
            exit(0)
