list = [input().split(': ') for s in range(int(input()))]
for word in list:
    word[0] = word[0].lower()
mytuple = tuple(list)
dict = dict(mytuple)


list_out = [input().lower() for s in range(int(input()))]
for s in list_out:
    if s not in dict:
        print('Не найдено')
    else:
        print(dict[s])
