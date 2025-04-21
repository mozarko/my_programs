from fractions import Fraction as F
from math import gcd

n = int(input())

numenat = n // 2
denominat = n - numenat

while gcd(numenat, denominat) != 1:
    numenat -= 1
    denominat += 1
print(F(numenat, denominat))
