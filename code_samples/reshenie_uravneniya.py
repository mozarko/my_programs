total = 0
for n in range(1, 20):
    for k in range(1, 20):
        for m in range(1, 20):
            if 28*n + 30*k + 31*m == 365:
                total += 1
                print('n =', n, 'k =', k, 'm =', m)
print('Общее количество натуральных решений =', total)