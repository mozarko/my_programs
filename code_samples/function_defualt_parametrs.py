def matrix(l=1, k=0, v=0, mt=[]):
    if k == 0 and v == 0:
        mt = [[0] * l] * l
        return mt
    if k > 0 and v == 0:
        mt = [[0] * k] * l
        return mt
    if v != 0:
        mt = [[v] * k] * l
        return mt


print(matrix(3,1))
