color1 = str(input())
color2 = str(input())

# если смешать красный и синий, то получится фиолетовый;
# если смешать красный и желтый, то получится оранжевый;
# если смешать синий и желтый, то получится зеленый.

def correct_colors():
    if (color1 == 'красный' or color1 == 'синий' or color1 == 'желтый') and (
            color2 == 'красный' or color2 == 'синий' or color2 == 'желтый'):
        return 1
    else:
        return 0


def colors_mix():
    if color1 == color2:
        return color1
    elif (color1 == 'красный' and color2 == 'синий') or (color2 == 'красный' and color1 == 'синий'):
        return 'фиолетовый'
    elif (color1 == 'красный' and color2 == 'желтый') or (color2 == 'красный' and color1 == 'желтый'):
        return 'оранжевый'
    elif (color1 == 'синий' and color2 == 'желтый') or (color2 == 'синий' and color1 == 'желтый'):
        return 'зеленый'


if correct_colors() == 0:
    print('ошибка цвета')
else:
    print(colors_mix())
