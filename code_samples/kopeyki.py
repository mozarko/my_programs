string = input()

count = 0
for s in string:
    count += 60
rub = count // 100
if count >= 100:
    kop = str(count)
    kop_str = kop[-2] + kop[-1]
    kop_int = int(kop_str)

else:
    kop_int = count

print(f'{rub} р. {kop_int} коп.')
