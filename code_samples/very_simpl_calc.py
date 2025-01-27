a = int(input())
b = int(input())
znak = str(input())

if b == 0 and znak == '/':
    print(f'На ноль делить нельзя!')
elif znak == '+' or znak == '-' or znak == '*' or znak == '/':
    x = str(a)+str(znak)+str(b)
    print(eval(x))
else:
    print(f'Неверная операция')