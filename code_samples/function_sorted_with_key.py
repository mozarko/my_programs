s = input()
mylist = s.split()


def f(word):
    new_list = []
    new_list.append(word)
    for i in range(len(new_list)):
        new_list[i] = new_list[i].lower()
    new_list.sort()
    return new_list


print(*sorted(mylist, key=f))
