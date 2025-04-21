from operator import *


def arithmetic_operation(simv):
    kw = {"+": add,
          "-": sub,
          "*": mul,
          "/": truediv}
    return lambda x, y: kw[simv](x, y)


add = arithmetic_operation('+')
div = arithmetic_operation('/')
print(add(10, 20))
print(div(20, 5))
