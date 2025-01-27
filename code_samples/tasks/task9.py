ppow, point = input().split()
ppow = int(ppow)
point = float(point)

coeff = []

for _ in range(ppow + 1):
    coeff.append(float(input()))

derivative = 0.0
for i in range(1, ppow + 1):
    derivative += (ppow - (i - 1)) * coeff[i - 1] * pow(point, ppow - i)

print(f'{derivative:.3f}', end="")
