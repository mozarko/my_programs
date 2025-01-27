string = input()
list = [s for s in string]

def_list = [input().split(': ') for s in range(int(input()))]
def_dict = {}
for s in def_list:
    def_dict[s[0]] = def_dict.get(s[0], int(s[1]))

for s in string:
    for key, value in def_dict.items():
        if string.count(s) == value:
            print(key, end='')
