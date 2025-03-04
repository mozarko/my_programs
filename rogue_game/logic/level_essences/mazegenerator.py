from __future__ import annotations
from random import choice, sample, randint


class MazeGenerator:
    def __init__(self):
        # Матрица доступа между комнатами
        self.struct_maze = {
            0: [1, 3],
            1: [0, 2, 4],
            2: [1, 5],
            3: [0, 4, 6],
            4: [1, 3, 5, 7],
            5: [2, 4, 8],
            6: [3, 7],
            7: [4, 6, 8],
            8: [5, 7]
        }

    def create_path(self, rooms_to_process: list[int]) -> tuple[list[int], list[int]]:
        """
        Генерирует одиночный путь для лабиринта, на основе списка комнат.

        Args:
            rooms_to_process (list[int]): Список комнат, из которых будет строиться путь.

        Returns:
            tuple[list[int], list[int]]: Список необработанных комнат и построенный путь.
        """
        current_path = []
        # Если список построенного лабиринта с комнатами пустой, выбираем произвольную комнату из списка доступных комнат
        # Если в списке лабиринта уже есть комната, то выбираем произвольную комнату из списка доступных комнат,
        # в которую можно поспасть из последней комнаты в построенном лабиринте.
        while rooms_to_process:
            if not current_path:
                room_number = choice(rooms_to_process)
                current_path.append(room_number)
                rooms_to_process.remove(room_number)
            else:
                connected_rooms = [room for room in rooms_to_process if room in self.struct_maze[current_path[-1]]]
                if not connected_rooms:
                    break

                room_number = choice(connected_rooms)
                current_path.append(room_number)
                rooms_to_process.remove(room_number)
        # Если список комнат для обработки не пустой, проверяем, можем ли мы какую-то из этих комнат добавить
        # в начало списка лабиринта.
        if rooms_to_process:
            for room_number in rooms_to_process:
                if current_path[0] in self.struct_maze[room_number]:
                    current_path.insert(0, room_number)
                    rooms_to_process.remove(room_number)
                    break

        return rooms_to_process, current_path

    def create_seq_maze(self) -> list[tuple[int, int]]:
        """
        Генерирует связный лабиринт, соединяя все комнаты.

        Returns:
            list[tuple[int, int]]: Список путей, где каждый путь — последовательность соединённых комнат.
        """
        rooms_to_process = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        all_paths = []
        # Создаем лабиринт из комнат, пока список комнат, доступных для связывания, не пустой
        while rooms_to_process:
            rooms_to_process, path = self.create_path(rooms_to_process)
            all_paths.append(path)
        # Если не удалось составить один лабиринт из комнат, то связываем оставшиеся лабиринты с первым
        if len(all_paths) > 1:
            for i in range(1, len(all_paths)):
                for room_number in all_paths[0]:
                    if room_number in self.struct_maze[all_paths[i][0]]:
                        all_paths[i].insert(0, room_number)
                        break
                    if room_number in self.struct_maze[all_paths[i][-1]]:
                        all_paths[i].append(room_number)
                        break

        pairs_rooms = self.transform_to_pair(all_paths)
        pairs_rooms = self.add_bonus_rooms(pairs_rooms)
        return pairs_rooms

    def transform_to_pair(self, all_paths: list[list[int]]) -> list[list[int]]:
        """
        Преобразует список лабиринта в список пар комнат, идущих по порядку.

        Args:
            all_paths list[list[int]]: Список лабиринта из номеров комнат.

        Returns:
            list[list[int]]: список пар комнат лабиринта, идущих по порядку.
        """
        return [[sublist[i], sublist[i+1]] for sublist in all_paths for i in range(len(sublist)-1)]

    def get_free_rooms(self, pairs_rooms: list[tuple[int, int]]) -> list[list[int]]:
        """
        Возвращает список комнат, которые не учавствуют в списке лабиринта комнат.

        Args:
            pairs_rooms list[tuple[int, int]]: Список лабиринта из номеров комнат, которые будут соеденяться коридорами.

        Returns:
            list[list[int]]: список комнат, которые не учавствуют в списке лабиринта комнат.
        """
        free_rooms = []
        # Цикл проходится по всем парам номеров комнат, из которых убираются пары комнат, которые невозможно соеденить коридорами,
        # затем убираются пары комнат, которые уже содержатся в списке лабиринта.
        for i, t in ((i, t) for i in range(9) for t in range(9) if i != t):
            if (t in self.struct_maze[i] or i in self.struct_maze[t]) and sorted([i, t]) not in (free_rooms + [sorted(sublist) for sublist in pairs_rooms]):
                free_rooms.append(sorted([i, t]))

        return free_rooms

    def add_bonus_rooms(self, pairs_rooms) -> list[tuple[int, int]]:
        """
        Добавляет в список лабиринта случайные пары комнат, которые не учавствуют в списке лабиринта.
        Args:
            pairs_rooms list[tuple[int, int]]: Список лабиринта из номеров комнат, которые будут соеденяться коридорами.
        Returns:
            list[tuple[int, int]]: Новый список лабиринта из номеров комнат.
        """
        for pair_room in sample(self.get_free_rooms(pairs_rooms), randint(1, len(self.get_free_rooms(pairs_rooms))-1)):
            pairs_rooms.append(pair_room)
        return pairs_rooms
