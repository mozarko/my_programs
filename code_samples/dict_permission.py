my_dict_prava = {}
dict_perm = {'write': 'W', 'read': 'R', 'execute': 'X'}
for _ in range(int(input())):
    s = input().split()
    my_dict_prava[s[0]] = s[1:]

list_files = []

for _ in range(int(input())):
    s = input().split()
    list_files.append(s)

for list in list_files:
    list[0] = dict_perm[list[0]]

for list in list_files:
    if list[0] in my_dict_prava[list[1]]:
        print('OK')
    else:
        print('Access denied')
