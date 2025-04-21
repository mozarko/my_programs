my_list = [i for i in range(1, int(input()) + 1)]
my_dict = {}
for i in range(len(my_list)):
    s = sum(map(int, list(str(my_list[i]))))
    my_dict[s] = my_dict.get(s, 0) + 1

maximum = 0
for value in my_dict.values():
    if value > maximum:
        maximum=value
print(maximum)
