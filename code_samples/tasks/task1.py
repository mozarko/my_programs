vector_1 = input().split()
vector_2 = input().split()

x1, y1, z1 = map(float, vector_1)
x2, y2, z2 = map(float, vector_2)

print(x1 * x2 + y1 * y2 + z1 * z2, end="")
exit(0)
