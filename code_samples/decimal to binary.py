a = int(input())
bn = ''
while a != 0:
    bn = str(a % 2) + bn
    a //= 2
print(bn)
