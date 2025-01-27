with open('files.txt', encoding='utf-8') as file:
    content = list(map(str.strip, file.readlines()))


def sum_group(num_size, byte_size):
    num_size = int(num_size)
    if byte_size == 'B':
        return num_size
    if byte_size == 'KB':
        return num_size * 1024
    if byte_size == "MB":
        return num_size * 1024 * 1024
    if byte_size == 'GB':
        return num_size * 1024 * 1024 * 1024


dict_rash = {}
for el in content:
    rash = el[el.find('.'):el.find(' ')]
    dict_rash[rash] = dict_rash.get(rash, 0)
group_list = [[] for _ in range(len(dict_rash))]
dict_rash = dict(sorted(dict_rash.items()))
i = 0
for key in dict_rash:
    for el in content:
        if key in el:
            group_list[i].append(el)
    i += 1

for i in range(len(group_list)):
    for el in group_list[i]:
        rash = el[el.find('.'):el.find(' ')]
        size = el[el.find(' ') + 1:]
        num_size = size[:size.find(' ')]
        byte_size = size[size.find(' ') + 1:]
        dict_rash[rash] = dict_rash.get(rash, 0) + sum_group(num_size, byte_size)

for key, value in dict_rash.items():
    count_bytes = 0
    while value > 1023:
        value = int(round((value / 1024), 0))
        count_bytes += 1
    match count_bytes:
        case 0:
            value = str(value) + ' B'
        case 1:
            value = str(value) + ' KB'
        case 2:
            value = str(value) + ' MB'
        case 3:
            value = str(value) + ' GB'
    dict_rash[key] = value

for el in group_list:
    el.sort()
    for i in range(len(el)):
        el[i]=el[i][:el[i].find(' ')]

for i in range(len(group_list)):
    for el in group_list[i]:
        rash = el[el.find('.'):]
        print(el, sep='\n')
    print(f'----------')
    print(f'Summary: {dict_rash[rash]}')
    print()
