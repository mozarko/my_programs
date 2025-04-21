import random


def gen_secret_friend():
    friends = []
    n = int(input())
    for _ in range(n):
        friends.append(input())
    secret_friends = friends.copy()
    count = n - 1
    while count < n:
        random.shuffle(secret_friends)
        for i in range(len(friends)):
            if friends[i] == secret_friends[i]:
                count = 0
            else:
                count += 1
    for i in range(len(friends)):
        print(f'{friends[i]} - {secret_friends[i]}')


gen_secret_friend()
