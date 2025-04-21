s = input()

counter = 0
for i in s:
    if i == 'f':
        counter += 1

if counter == 1:
    print('-1')
if counter == 0:
    print('-2')
if counter >= 2:
    pos = s.find('f', s.find('f') + 1)
    print(pos)
