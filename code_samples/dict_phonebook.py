list = [input().split() for s in range(int(input()))]
for i in range(len(list)):
    list[i][0], list[i][1] = list[i][1].lower(), list[i][0]
dict = {}
for word in list:
    if word[0] in dict:
        dict[word[0]] = dict[word[0]] + ' ' + word[1]
    dict[word[0]] = dict.get(word[0], word[1])

friend_list = [input().lower() for s in range(int(input()))]
for friend in friend_list:
    if friend in dict:
        print(dict[friend])
    else:
        print('абонент не найден')

