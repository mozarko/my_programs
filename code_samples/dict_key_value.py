mytuple = (input().split() for s in range(int(input())))
dict = dict(mytuple)

s = input()
for key, value in dict.items():
    if key == s:
        print(value)
    if value == s:
        print(key)
