import random
import string


def gen_password_all():
    s1 = string.ascii_letters
    s2 = string.digits
    s3 = s1 + s2
    my_list = []
    ignore_list = ['l', 'I', '1', 'o', 'O', '0']
    for s in s3:
        if s not in ignore_list:
            my_list.append(s)
    return my_list


def gen_password_type(t):
    s1 = string.ascii_lowercase
    s2 = string.ascii_uppercase
    s3 = string.digits
    my_list = []
    ignore_list = ['l', 'I', '1', 'o', 'O', '0']
    if t == "lower":
        for s in s1:
            if s not in ignore_list:
                my_list.append(s)
        return my_list
    if t == 'upper':
        for s in s2:
            if s not in ignore_list:
                my_list.append(s)
        return my_list
    if t == 'digit':
        for s in s3:
            if s not in ignore_list:
                my_list.append(s)
        return my_list


def generate_password(length):
    if length == 3:
        s = random.choice(gen_password_type('lower')) + random.choice(gen_password_type('upper')) + random.choice(
            gen_password_type('digit'))
        return s
    if length > 3:
        s = random.choice(gen_password_type('lower')) + random.choice(gen_password_type('upper')) + random.choice(
            gen_password_type('digit'))
        for _ in range(length - 3):
            s += random.choice(gen_password_all())
        return s


def generate_passwords(count, length):
    for _ in range(count):
        print(generate_password(length))


n, m = int(input()), int(input())
generate_passwords(n, m)
