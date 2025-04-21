from math import sin
from math import sqrt


def pw(n):
    return n**2
def cub(n):
    return n**3
def sqrtt(n):
    return sqrt(n)
def abss(n):
    return abs(n)
def sinus(n):
    return sin(n)


commands = {'квадрат': pw, 'куб': cub, 'корень': sqrtt, 'модуль': abss, 'синус': sinus}

n = int(input())
comand = input()

print(commands[comand](n))