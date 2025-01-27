number = int(input())

# карман 0 зеленый;
# для карманов с 1 по 10 карманы с нечетным номером имеют красный цвет, карманы с четным номером – черный;
# для карманов с 11 по 18 карманы с нечетным номером имеют черный цвет, карманы с четным номером – красный;
# для карманов с 19 по 28 карманы с нечетным номером имеют красный цвет, карманы с четным номером – черный;
# для карманов с 29 по 36 карманы с нечетным номером имеют черный цвет, карманы с четным номером – красный.


def chet_number():
    if 0 <= number <= 36:
        if number % 2 == 0 or number == 0:
            return 'chet'
        else:
            return 'nechet'
    else:
        return 'wrong'


def opred_number():
    if chet_number() == 'chet':
        if 1 <= number <= 10 or 19 <= number <= 28:
            return 'черный'
        elif 11 <= number <= 18 or 29 <= number <= 36:
            return 'красный'
        elif number == 0:
            return 'зеленый'
    elif chet_number() == 'nechet':
        if 1 <= number <= 10 or 19 <= number <= 28:
            return 'красный'
        elif 11 <= number <= 18 or 29 <= number <= 36:
            return 'черный'


if chet_number() != 'wrong':
   print(opred_number())
else:
    print('ошибка ввода')
