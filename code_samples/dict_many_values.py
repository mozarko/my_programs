mylist = [input().split() for s in range(int(input()))]

dict = {}
for list in mylist:
    dict[list[0]] = dict.get(list[0], list[1:])

city_list = [input() for s in range(int(input()))]
for city in city_list:
    for key, value in dict.items():
        if city in value:
            print(key)