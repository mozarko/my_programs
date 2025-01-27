def gem(word):
    my_list = word.split('.')
    my_list = [int(i) for i in my_list]
    total = 0
    for i in range(len(my_list)):
        total += my_list[i] * 256 ** (len(my_list) - 1 - i)
    return total


my_list = [input() for s in range(int(input()))]
print(*sorted(my_list,key=gem),sep='\n')
