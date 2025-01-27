athletes = [('Дима', 10, 130, 35), ('Тимур', 11, 135, 39), ('Руслан', 9, 140, 33), ('Рустам', 10, 128, 30),
            ('Амир', 16, 170, 70), ('Рома', 16, 188, 100), ('Матвей', 17, 168, 68), ('Петя', 15, 190, 90)]


def sort_by_param(n):
    def param(athl_tpl):
        return athl_tpl[n - 1]
    return param

for el in sorted(athletes, key=sort_by_param(int(input()))):
    print(*el)
