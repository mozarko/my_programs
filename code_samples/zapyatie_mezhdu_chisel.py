def sac(num):
    if num >= 1000:
        k = ''
        count = 0
        s = str(num)
        for _ in range(len(s) // 2):
            k += s[(-1 - count):(-4 - count):-1] + ','
            count += 3
        k = k[::-1]
        k = k.lstrip(',')
        print(k)
    else:
        print(num)


number = int(input())

sac(number)
