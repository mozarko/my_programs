import curses
import math

MAX_LEVELS = 21
BACKPACK_MAX_SIZE = 9
MAP_WIDTH = 60
MAP_HEIGHT = 20
MAX_ROOM_SIZE = 18
MIN_ROOM_SIZE = 5
MAX_ROOMS = 9
MIN_LVL_ENEMIES_NUM = 5
MAX_LVL_ENEMIES_NUM = 20

# For 3D
FOV = math.pi / 3
HALF_FOV = FOV / 2


# Control keys
KEY_UP = [curses.KEY_UP, ord('w')]
KEY_DOWN = [curses.KEY_DOWN, ord('s')]
KEY_ENTER = [curses.KEY_ENTER, 10, 13]
KEY_ESC = 27
KEY_SPACE = 32
KEY_OPEN_BACKPACK = 9
KEY_CONFIRM = [ord('y'), ord('Y')]
KEY_MODE_3D = [ord('z'), ord('Z')]

DIRECTION_MAP = {
    'w': (0, -1),  # Вверх: уменьшаем y
    's': (0, 1),   # Вниз: увеличиваем y
    'd': (1, 0),   # Вправо: увеличиваем x
    'a': (-1, 0),  # Влево: уменьшаем x
}

# Список врагов
ENEMY_LIST = ["zombie", "vampire", "ghost", "ogre", "snake_mage", "mimik"]

# Конфигурация для всех атрибутов (слабый, средний, сильный, очень сильный)
ATTRIBUTE_CONFIG = {
    "weak": {
        "health": 50,
        "agility": 5,
        "strength": 7,
        "hostility": 2
    },
    "medium": {
        "health": 70,
        "agility": 7,
        "strength": 12,
        "hostility": 3
    },
    "strong": {
        "health": 90,
        "agility": 10,
        "strength": 15,
        "hostility": 4
    },
    "very_strong": {
        "health": 100,
        "agility": 15,
        "strength": 20,
        "hostility": 5
    }
}


RARITY_MODIFIERS = {
    'common': 1,
    'rare': 2,
    'legendary': 5
}

RARITY_PROBABILITIES = {
    'common': 65,    # 65% вероятность
    'rare': 30,      # 30% вероятность
    'legendary': 5   # 5% вероятность
}

ITEM_TYPES = {'treasure': '$', 'food': '♥',
              'elixir': '✚', 'scroll': '~', 'sword': '†'}

ITEM_USE = {'h': ["sword", "equip"], 'j': ["food", "eat"],
            'k': ["elixir", "use"], 'e': ["scroll", "use"]}

BUFF_DUR = 30


DODGE_COEFFICIENT = 0.3
MAX_DODGE_CHANCE = 70


MIN_ITEM_ON_MAP_EXCEPT_SWORD_AND_FOOD = 5
MAX_ITEM_ON_MAP_EXCEPT_SWORD_AND_FOOD = 10

MIN_FOOD_ON_MAP = 5
MAX_FOOD_ON_MAP = 8
MIN_FOOD_IN_START_ROOM = 1

EXIT_DOOR = '■'

COLOR_KEY_DOOR = [3, 2, 7]


# коэффициенты генерации предметов, врагов и их статов
LVL_GEN_COEF = {
    "enemies_count": 1.0,
    "enemies_health_stats": 1.0,
    "items_count": 1.0,
    "items_healing": 1.0,
}


SAVE_FILE_PATH = "datalayer/saving.json"
STATS_FILE_PATH = "datalayer/statistics.json"
