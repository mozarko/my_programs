def check_five(n):
    result = []
    mylist = [[] for _ in range(n)]
    for i in range(n):
        for _ in range(int(input())):
            s = input()
            mylist[i].append(s)
    for list in mylist:
        for el in list:
            if el[-1] == '5':
                result.append(True)
                break
        else:
            result.append(False)
    return 'YES' if all(result) else 'NO'


n = int(input())
print(check_five(n))
