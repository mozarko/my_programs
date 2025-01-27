from datetime import date


def saturdays_between_two_dates(date1, date2):
    dates = [date1, date2]
    dates.sort()
    start, end = dates[0], dates[1]
    time_delta = end.toordinal() - start.toordinal()
    saturdays = 0
    for i in range(time_delta + 1):
        if date.fromordinal(start.toordinal() + i).isoweekday() == 6:
            saturdays += 1
    return saturdays


date1 = date(2021, 11, 1)
date2 = date(2021, 11, 22)

print(saturdays_between_two_dates(date1, date2))

date1 = date(2020, 7, 26)
date2 = date(2020, 7, 2)

print(saturdays_between_two_dates(date1, date2))

date1 = date(2018, 7, 13)
date2 = date(2018, 7, 13)

print(saturdays_between_two_dates(date1, date2))
