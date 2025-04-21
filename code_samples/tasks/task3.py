def is_figure(i, j, count):
    check = 0;
    global circles
    global squares
    if count == 1 and (j == 0 or j == 9):
        exit(0)

    if count == 1:
        for k in range(3):
            if matrix[i + 1][j + k - 1] == 1:
                visited[i + 1][j + k - 1] = True
                check += 1
        if matrix[i + 2][j] == 1:
            visited[i + 2][j] = True
            check += 1
        if check == 4:
            circles += 1

    if count == 3:
        for k in range(3):
            if matrix[i + 1][j + k] == 1:
                visited[i + 1][j + k] = True
                check += 1
            if matrix[i + 2][j + k] == 1:
                visited[i + 2][j + k] = True
                check += 1
        if check == 6:
            squares += 1

    if count == 2 and matrix[i + 1][j + 2] == 0:
        for k in range(2):
            if matrix[i + 1][j + k] == 1:
                visited[i + 1][j + k] = True
                check += 1
        if check == 2:
            squares += 1

    if count == 2 and matrix[i + 1][j + 2] == 1:
        for k in range(4):
            if matrix[i + 1][j + k - 1] == 1:
                visited[i + 1][j + k - 1] = True
                check += 1
            if matrix[i + 2][j + k - 1] == 1:
                visited[i + 2][j + k - 1] = True
                check += 1
        for k in range(2):
            if matrix[i + 3][j + k] == 1:
                visited[i + 3][j + k] = True
                check += 1
        if check == 10:
            circles += 1


matrix = []
visited = []

with open('input_task3.txt', 'r') as f:
    for line in f:
        matrix.append([int(x) for x in line.split()])
for i in range(len(matrix)):
    visited.append([False] * len(matrix[0]))
count = 0
circles = 0
squares = 0
for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        if matrix[i][j] == 1 and visited[i][j] == False:
            count += 1
        if matrix[i][j] == 0 and count > 0:
            is_figure(i, j - count, count)
            count = 0

print(squares, circles, end="")
