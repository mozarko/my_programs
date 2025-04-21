weight = 100
height = 1.77

def bmi(weight, height):
    index = (weight / (height * height))
    if index <= 18.5:
        return 'Underweight'
    if 18.5 < index <= 25:
        return 'Normal'
    if 25 < index <= 30:
        return 'Overweight'
    if index > 30:
        return 'Obese'


print(bmi(weight, height))
