s = str(input())

num = 0
sign = 1
frac = 0
error = False
has_frac = False
for i, c in enumerate(s):
    if c == '-':
        sign = -1
    elif c == '.':
        has_frac = True
    elif c.isdigit():
        if has_frac:
            frac = frac * 10 + ord(c) - ord('0')
        else:
            num = num * 10 + ord(c) - ord('0')
    else:
        error = True
if error:
    print('n/a', end='')
    exit(1)

if has_frac:
    print(f'{sign * (num + frac / 10 ** len(str(frac))) * 2:.3f}', end='')
else:
    print(f'{sign * num * 2:.3f}', end='')
exit(0)
