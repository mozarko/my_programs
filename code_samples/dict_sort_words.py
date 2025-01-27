s = input().lower()


def repl(s):
    s = s.replace(',', '')
    s = s.replace('!', '')
    s = s.replace('+', '')
    s = s.replace('=', '')
    s = s.replace('?', '')
    s = s.replace('.', '')
    s = s.replace('-', '')
    return s


s = repl(s)
list = s.split()

dict = {}
count = 0
for i in range(len(list)):
    for key in list:
        if list[i] == key:
            count += 1
    dict.setdefault(list[i], count)
    count = 0
min = 1000
for key in dict:
    if dict[key] < min:
        min = dict[key]
result_list = []
for key, values in dict.items():
    if values == min:
        result_list.append(key)
result_list.sort()

print(result_list[0])