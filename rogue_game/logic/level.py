from __future__ import annotations
import random

from constants.game_constants import *
from logic.level_essences.corridor import Corridor
from logic.level_essences.key import Key
from logic.level_essences.door import Door
from logic.level_essences.mazegenerator import MazeGenerator
from logic.level_essences.room import Room
from logic.level_essences.tile import Tile
from logic.character import Character
from logic.enemy_factory import EnemyFactory
from logic.item import Item


class Level:
    def __init__(self):
        self.tiles = self.__initialize_tiles()
        self.exit_door_x = 0
        self.exit_door_y = 0
        self.rooms = []
        self.corridors = []
        self.maze_path = []
        self.doors = {}
        self.keys = {}
        self.visited_corridors = set()

    def __initialize_tiles(self):
        tiles = [[Tile(True) for _ in range(MAP_HEIGHT)]
                 for _ in range(MAP_WIDTH)]

        return tiles

    def __create_room(self, room: Room):
        for x in range(room.x1, room.x2 + 1):
            for y in range(room.y1, room.y2 + 1):
                self.tiles[x][y].blocked = False

    def __filling_room(self, enemies: list[EnemyFactory], items: list[Item], start_room_idx: int):
        food_in_start_room = MIN_FOOD_IN_START_ROOM
        for item in items:
            room = random.choice(self.rooms)
            if item.item_type == "food" and food_in_start_room > 0:
                item.x = random.randint(
                    self.rooms[start_room_idx].x1, self.rooms[start_room_idx].x2)
                item.y = random.randint(
                    self.rooms[start_room_idx].y1, self.rooms[start_room_idx].y2)
                food_in_start_room -= 1
            else:
                item.x = random.randint(room.x1, room.x2)
                item.y = random.randint(room.y1, room.y2)

        for enemy in enemies:
            room = random.choice(
                [room for room in self.rooms if room != self.rooms[start_room_idx]])
            enemy.x = random.randint(room.x1, room.x2)
            enemy.y = random.randint(room.y1, room.y2)

    def create_lvl(self, player: Character, enemies: list[EnemyFactory], items: list[Item]):
        self.generate_rooms()

        start_room_idx = random.randint(0, MAX_ROOMS - 1)
        player.x = random.randint(
            self.rooms[start_room_idx].x1 + 1, self.rooms[start_room_idx].x2 - 1)
        player.y = random.randint(
            self.rooms[start_room_idx].y1 + 1, self.rooms[start_room_idx].y2 - 1)

        [self.exit_door_x, self.exit_door_y] = random.choice(
            [room for room in self.rooms if room != self.rooms[start_room_idx]]).generate_exit()

        self.__filling_room(enemies, items, start_room_idx)

        self.create_corridors()
        self.create_doors()
        self.create_keys(start_room_idx)
        self.set_corridors()
        self.update_fog_of_war()
        self.clear_fog_room(self.rooms[start_room_idx])

    def bresenham(self, x0: int, y0: int, x1: int, y1: int) -> list[tuple[int, int]]:
        """
        Реализует алгоритм Брезенхэма для рисования линии между двумя точками.
        Args:
            x0 (int): Координата x первой точки.
            y0 (int): Координата y первой точки.
            x1 (int): Координата x второй точки.
            y1 (int): Координата y второй точки.
        Returns:
            list[tuple[int, int]]: Список координат точек линии.
        """
        points = []  # Список для хранения координат точек линии
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy

        while True:
            points.append((x0, y0))  # Добавляем текущую точку в список

            # Если достигли второй точки, выходим
            if x0 == x1 and y0 == y1:
                break

            e2 = err * 2
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

        return points

    def ray_casting(self, x: int, y: int, angle: float, max_distance: int = 10):
        """
        Реализует алгоритм рейкастинга для определения видимости в игре.
        Args:
            x (int): Координата x начальной точки луча.
            y (int): Координата y начальной точки луча.
            angle (float): Угол направления луча.
            max_distance (int, optional): Максимальное расстояние, на котором луч может достигнуть. По умолчанию 10.
        """
        # Переводим угол в радианы и ищем конечные координаты луча с помощью Брейзенхема
        for depth in range(0, max_distance):
            ray_x = int(x + depth * math.cos(angle))
            ray_y = int(y + depth * math.sin(angle))

            # Применяем алгоритм Брейзенхема для нахождения всех точек на пути луча
            points = self.bresenham(x, y, ray_x, ray_y)

            # Проверяем, не выходим ли за границы экрана
            for (rx, ry) in points:
                if rx < 0 or rx >= MAP_WIDTH or ry < 0 or ry >= MAP_HEIGHT:
                    break

                self.tiles[rx][ry].block_sight = False

                if (rx, ry) in set((x, y) for corr in self.corridors for x, y in corr.coordinates):
                    self.visited_corridors.add((rx, ry))

                if self.tiles[rx][ry].blocked:
                    break

    def update_fog_of_war(self):
        """
        Обновляет состояние "тумана войны" на карте.
        Если ячейка не заблокирована, то она становится невидимой.
        """
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                if not self.tiles[x][y].blocked:
                    self.tiles[x][y].block_sight = True

    def clear_fog_of_war(self, x: int, y: int):
        """
        Снимает "туман войны" вокруг точки с координатами (x, y).
        Args:
            x (int): Координата x точки.
            y (int): Координата y точки.
        """
        self.update_fog_of_war()
        self.clear_fog_rooms(x, y)
        # Смотрим вокруг себя по всей окружности
        for angle_offset in range(0, 360, 5):
            ray_angle = math.radians(angle_offset)
            self.ray_casting(x, y, ray_angle)

    def clear_fog_rooms(self, x: int, y: int):
        """
        Если координаты (x, y) находятся в комнате, снимает "туман войны" со всей этой комнаты.
        Args:
            x (int): Координата x точки.
            y (int): Координата y точки.
        """
        for room in self.rooms:
            if room.is_room(x, y):
                self.clear_fog_room(room)
                break

    def clear_fog_room(self, room: Room):
        """
        Очищает "туман войны" в комнате.
        Args:
            room (Room): Комната, в которой нужно очистить "туман войны".
        """
        for x in range(max(room.x1 - 1, 0), min(room.x2 + 2, MAP_WIDTH)):
            for y in range(max(room.y1 - 1, 0), min(room.y2 + 2, MAP_HEIGHT)):
                self.tiles[x][y].block_sight = False

    def create_doors(self):
        """
        Функция создает цветные двери между комнатами.
        """
        for color_idx in COLOR_KEY_DOOR:
            door = Door(color_idx, self.get_free_corridors())
            self.doors.update({door.color_idx: door})

    def create_keys(self, start_room_idx: int):
        """
        Функция создает цветные ключи в комнатах используя алгоритм обхода графа лабиринта.
        Args:
            start_room_idx int: Номер стартовой комнаты.
        """
        # Чтобы не менять оригинальный массив, берем копию
        temp_maze = self.maze_path.copy()
        # Из массива лабиринта убираем коридоры, которые закрыты дверьми
        for door in self.doors.values():
            pair_rooms = [door.corridor.rooms[0].room_number,
                          door.corridor.rooms[1].room_number]
            if pair_rooms not in temp_maze:
                pair_rooms.reverse()
            temp_maze.remove(pair_rooms)
        # Для каждого цвета получаем список доступных комнат и в произвольной создаем ключ
        for color_idx in self.get_sorted_color_list(start_room_idx):
            available_rooms = set()
            self.get_available_rooms(
                temp_maze, start_room_idx, available_rooms)
            key = Key(color_idx, [self.rooms[i] for i in available_rooms])
            # Добавляем в массив лабиринта коридор, который можно открыть ключем
            temp_maze.append([self.doors[color_idx].corridor.rooms[0].room_number,
                              self.doors[color_idx].corridor.rooms[1].room_number])
            self.keys.update({key.color_idx: key})

    def get_sorted_color_list(self, start_room_idx: int):
        """
        Функция создает список цветов ключей упорядоченных по близости коридора данного цвета к стартовой комнате.
        Args:
            start_room_idx int: Номер стартовой комнаты.
        Returns:
            list[int]: Отсортированый список цветов.
        """
        sorted_map = {}
        # Для текущего цвета из списка путей убираем его коридор и смотрим во сколько комнат можно попасть.
        for color_idx in COLOR_KEY_DOOR:
            temp_maze = self.maze_path.copy()

            pair_rooms = [self.doors[color_idx].corridor.rooms[0].room_number,
                          self.doors[color_idx].corridor.rooms[1].room_number]
            if pair_rooms not in temp_maze:
                pair_rooms.reverse()
            temp_maze.remove(pair_rooms)

            available_rooms = set()
            self.get_available_rooms(
                temp_maze, start_room_idx, available_rooms)
            # Добавляем в словарь номер цвета и количество доступных комнат
            sorted_map.update({color_idx: len(available_rooms)})
        # Сортируем словарь по значениям и возвращаем список ключей
        return [key for key, _ in sorted(sorted_map.items(), key=lambda x: x[1])]

    def get_available_rooms(self, maze: list[list[int]], room_number: int, available_rooms: set[int]):
        """
        Функция проходит по графу `maze` и возвращает список комнат, в которые можно дойти из комнаты с номером `room_number`.
        Args:
            maze list[list[int]]: Граф лабиринта.
            room_number int: Номер комнаты начальной позиции.
            available_rooms set[int]: Множество комнат в которые можно добраться из начальной комнаты.
        """
        available_rooms.add(room_number)
        for item in maze:
            if item[0] == room_number and item[1] not in available_rooms:
                self.get_available_rooms(maze, item[1], available_rooms)
            elif item[1] == room_number and item[0] not in available_rooms:
                self.get_available_rooms(maze, item[0], available_rooms)

    def get_free_corridors(self) -> list[Corridor]:
        """
        Возвращает список коридоров, в которых нет дверей.

        Returns:
            list[Corridor]: список коридоров, в которых нет дверей.
        """

        return [corr for corr in self.corridors if corr not in [
                door.corridor for door in self.doors.values()]]

    def block_door(self, door: Door):
        """
        Функция блокирует перемещение по коридорам с дверьми.
        Args:
            door Door: Дверь, перемещение сквозь которую будет блокироваться.
        """
        for x, y in door.corridor.coordinates:
            self.tiles[x][y].blocked = True

    def open_door(self, color_idx: int):
        """
        Функция открывает перемещение по коридорам с дверьми.
        Args:
            color_idx int: Цвет двери, которую нужно разблокировать
        """
        door = self.doors[color_idx]
        for x, y in door.corridor.coordinates:
            self.tiles[x][y].blocked = False

    def generate_rooms(self):
        """
        Функция генерации комнат на поле.
        """
        for i in range(MAX_ROOMS):
            w = random.randint(min(MIN_ROOM_SIZE, MAP_WIDTH // 3 - 1),
                               min(MAX_ROOM_SIZE, MAP_WIDTH // 3 - 1))
            h = random.randint(min(MIN_ROOM_SIZE, MAP_HEIGHT // 3 - 1),
                               min(MAX_ROOM_SIZE, MAP_HEIGHT // 3 - 1))
            x = random.randint((i % 3) * (MAP_WIDTH - 1) //
                               3 + 1, (i % 3 + 1) * (MAP_WIDTH - 1) // 3 - w)
            y = random.randint((i // 3) * (MAP_HEIGHT - 1) // 3 + 1,
                               (i // 3 + 1) * (MAP_HEIGHT - 1) // 3 - h)

            new_room = Room(x, y, w, h, i)
            self.__create_room(new_room)
            self.rooms.append(new_room)

    def set_corridors(self):
        """
        Функция регулирующая передвижение по коридорам.
        """
        for door in self.doors.values():
            self.block_door(door)

        for corr in self.get_free_corridors():
            for x, y in corr.coordinates:
                self.tiles[x][y].blocked = False

    def compelete_lvl(self, player: Character) -> bool:
        if self.exit_door_x == player.x and self.exit_door_y == player.y:
            return True
        return False

    def is_blocked(self, x, y) -> bool:
        if self.tiles[x][y].blocked:
            return True

        return False

    def create_corridors(self):
        """
        Функция создающая координаты коридоров.
        """
        # генерация пути для лабиринта из комнат
        self.maze_path = MazeGenerator().create_seq_maze()
        for path in self.maze_path:
            for i in range(len(path) - 1):
                corr = Corridor()
                # Если разница в номере комнат равна 1, то комнаты находятся на горизонтальной плоскости
                # Если нет, то друг над другом по вертикали.
                if abs(path[i] - path[i + 1]) == 1:
                    if self.rooms[path[i]].get_center()[0] > self.rooms[path[i + 1]].get_center()[0]:
                        corr.connect_horizontal_rooms(
                            self.rooms[path[i + 1]], self.rooms[path[i]])
                    else:
                        corr.connect_horizontal_rooms(
                            self.rooms[path[i]], self.rooms[path[i + 1]])
                else:
                    if self.rooms[path[i]].get_center()[1] > self.rooms[path[i + 1]].get_center()[1]:
                        corr.connect_vertical_rooms(
                            self.rooms[path[i + 1]], self.rooms[path[i]])
                    else:
                        corr.connect_vertical_rooms(
                            self.rooms[path[i]], self.rooms[path[i + 1]])
                self.corridors.append(corr)
