rows, cols = (map(int, input().split()))

matrix = [[0] * cols for i in range(rows)]

for i in range(rows):
    matrix[i] = list(map(int, input().split()))

cur_i, cur_j = 0, 0
coins = matrix[0][0]

while ((cur_i < rows - 1) and (cur_j < cols - 1)):
    if matrix[cur_i + 1][cur_j] >= matrix[cur_i][cur_j + 1]:
        coins += matrix[cur_i + 1][cur_j]
        cur_i += 1
    else:
        coins += matrix[cur_i][cur_j + 1]
        cur_j += 1

while (cur_i < rows - 1):
    coins += matrix[cur_i + 1][cur_j]
    cur_i += 1
while (cur_j < cols - 1):
    coins += matrix[cur_i][cur_j + 1]
    cur_j += 1

print(coins, end="")
