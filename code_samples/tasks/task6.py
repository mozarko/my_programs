import json
import sys


def read_input(filename):
    with open(filename, 'r') as file:
        data = file.read()
    return data


def validate_input(data):
    try:
        movies = json.loads(data)
        if not isinstance(movies, dict) or 'list1' not in movies or 'list2' not in movies:
            return False
        list1 = movies['list1']
        list2 = movies['list2']
        if not isinstance(list1, list) or not isinstance(list2, list):
            return False
        for movie_list in [list1, list2]:
            for movie in movie_list:
                if not isinstance(movie, dict) or 'title' not in movie or 'year' not in movie:
                    return False
                if not isinstance(movie['year'], int) or not isinstance(movie['title'], str):
                    return False
        return True
    except json.JSONDecodeError:
        return False


def merge_sorted_lists(list1, list2):
    merged = []
    i, j = 0, 0

    while i < len(list1) and j < len(list2):
        if list1[i]['year'] < list2[j]['year']:
            merged.append(list1[i])
            i += 1
        elif list1[i]['year'] > list2[j]['year']:
            merged.append(list2[j])
            j += 1
        else:
            merged.append(list1[i])
            merged.append(list2[j])
            i += 1
            j += 1

    while i < len(list1):
        merged.append(list1[i])
        i += 1

    while j < len(list2):
        merged.append(list2[j])
        j += 1

    return merged


def main():
    input_data = read_input('input_task6.txt')

    if not validate_input(input_data):
        print("Ошибка: некорректный ввод")
        return

    movie_lists = json.loads(input_data)
    list1, list2 = movie_lists['list1'], movie_lists['list2']

    merged_list = merge_sorted_lists(list1, list2)
    output = {"list0": merged_list}

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()