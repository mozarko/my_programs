from abc import ABC
from constants.game_constants import *
from logic.movement_strategies import *
from random import choice, randint, random


class EnemyFactory(ABC):
    """Абстрактный класс EnemyFactory"""

    def __init__(self, x, y, lvl_number, health, agility, strength, hostility, reward, symbol, movement_strategy,
                 color):
        self.x = x
        self.y = y
        self.lvl_number = lvl_number
        self.cur_hp = health  # Используем cur_hp вместо health
        self.max_hp = health  # Добавляем max_hp для отображения максимального здоровья
        self.agility = agility
        self.strength = strength
        self.hostility = hostility
        self.reward = reward
        self.symbol = symbol
        self.movement_strategy = movement_strategy
        self.color = color

    @classmethod
    def create_enemy(cls, lvl_number):
        enemy_type = choice(ENEMY_LIST)
        if enemy_type == "zombie":
            return Zombie(lvl_number)
        elif enemy_type == "vampire":
            return Vampire(lvl_number)
        elif enemy_type == "ghost":
            return Ghost(lvl_number)
        elif enemy_type == "ogre":
            return Ogre(lvl_number)
        elif enemy_type == "snake_mage":
            return SnakeMage(lvl_number)
        elif enemy_type == "mimik":
            return Mimik(lvl_number)

    def take_damage(self, damage: int):
        if hasattr(self, "dodge_first_attack"):
            if self.dodge_first_attack:
                return "dodge_first_attack"
        if randint(0, 100) <= self.calculate_dodge_chance():
            return "dodge"
        self.cur_hp -= damage
        return "ok"

    def is_dead(self) -> bool:
        return self.cur_hp <= 0

    def damage_calculation(self) -> int:
        return int(self.strength + randint(-5, 5))

    def calculate_dodge_chance(self):
        dodge_chance = self.agility * DODGE_COEFFICIENT
        return min(dodge_chance, MAX_DODGE_CHANCE)

    def _scale_attribute(self, base_value):
        """Метод для масштабирования характеристик"""
        return int(base_value * (1 + 0.1 * (self.lvl_number - 1)))

    def _set_param(self, health, agility, strength, hostility):
        """Метод получения параметров для всех атрибутов и масштабирования"""
        self.cur_hp = round(self._scale_attribute(
            ATTRIBUTE_CONFIG[health]["health"]) * LVL_GEN_COEF["enemies_health_stats"])
        self.max_hp = self.cur_hp
        self.agility = round(self._scale_attribute(
            ATTRIBUTE_CONFIG[agility]["agility"]) * LVL_GEN_COEF["enemies_health_stats"])
        self.strength = round(self._scale_attribute(
            ATTRIBUTE_CONFIG[strength]["strength"]) * LVL_GEN_COEF["enemies_health_stats"])
        self.hostility = ATTRIBUTE_CONFIG[hostility]["hostility"]
        self.reward = int((self.max_hp / 10 + self.agility +
                           self.strength + self.hostility * 5) / 2)


class Zombie(EnemyFactory):
    """Зомби (отображение: зеленый z): Низкая ловкость. Средняя сила, враждебность. Высокое здоровье."""

    def __init__(self, lvl_number):
        super().__init__(
            x=0, y=0, lvl_number=lvl_number,
            health=0, agility=0,
            strength=0, hostility=0, reward=0, symbol='z',
            movement_strategy=BasicMovementStrategy(), color=6
        )
        self._set_param(health="strong", agility="weak",
                        strength="medium", hostility="medium")

    def move(self, level, player_x, player_y):
        self.movement_strategy.move(self, level, player_x, player_y)

    def attack(self, player) -> str:
        damage = self.damage_calculation()
        attack_result = player.take_damage(damage)
        if attack_result == "dodge":
            return f"{player.player_name} dodged!"
        return f"Zombie attacks {player.player_name} for {damage} damage!"


class Vampire(EnemyFactory):
    """Вампир (отображение: красная v): Высокая ловкость, враждебность и здоровье. Средняя сила.
    Отнимает некоторое количество максимального уровня здоровья игроку при успешной атаке. Первый удар по вампиру — всегда промах."""

    def __init__(self, lvl_number):
        super().__init__(
            x=0, y=0, lvl_number=lvl_number,
            health=0, agility=0,
            strength=0, hostility=0, reward=0, symbol='v',
            movement_strategy=BasicMovementStrategy(), color=3
        )
        self._set_param(health="strong", agility="strong",
                        strength="medium", hostility="strong")

        self.dodge_first_attack = True  # Флаг уклонения от первого удара

    def move(self, level, player_x, player_y):
        self.movement_strategy.move(self, level, player_x, player_y)

    def attack(self, player) -> str:
        damage = self.damage_calculation()
        attack_result = player.take_damage(damage)
        if attack_result == "dodge":
            return f"{player.player_name} dodged!"
        reduce_max_hp = int(self.strength / 10 + randint(-3, 1))
        player.max_hp -= reduce_max_hp
        return f"Vampire attacks {player.player_name} for {damage} damage and reduces max HP for {reduce_max_hp}!"


class Ghost(EnemyFactory):
    """Привидение (отображение: белый g): Высокая ловкость. Низкая сила, враждебность и здоровье.
    Постоянно телепортируется по комнате и периодически становится невидимым, пока игрок не вступил в бой."""

    def __init__(self, lvl_number):
        super().__init__(
            x=0, y=0, lvl_number=lvl_number,
            health=0, agility=0,
            strength=0, hostility=0, reward=0, symbol='g',
            movement_strategy=GhostMovementStrategy(), color=1
        )
        self._set_param(health="weak", agility="strong",
                        strength="weak", hostility="weak")

        self.invisible = False  # Флаг невидимости

    def move(self, level, player_x, player_y):
        self.movement_strategy.move(self, level, player_x, player_y)

    def attack(self, player) -> str:
        damage = self.damage_calculation()
        attack_result = player.take_damage(damage)
        if attack_result == "dodge":
            return f"{player.player_name} dodged!"
        return f"Ghost attacks {player.player_name} for {damage} damage!"

    def set_symb(self):
        if self.invisible:
            self.symbol = '.'
            self.color = 6
        if not self.invisible:
            self.symbol = 'g'
            self.color = 1

    def check_invisible(self):
        if self.invisible:
            if random() < 0.7:
                self.invisible = False
                self.set_symb()
        if not self.invisible:
            if random() < 0.3:
                self.invisible = True
                self.set_symb()


class Ogre(EnemyFactory):
    """Огр (отображение: желтый O): Очень высокая сила и здоровье, низкая ловкость. Средняя враждебность.
    Ходит по комнате на две клетки, но после каждой атаки отдыхает один ход, затем гарантированно контратакует."""

    def __init__(self, lvl_number):
        super().__init__(
            x=0, y=0, lvl_number=lvl_number,
            health=0, agility=0,
            strength=0, hostility=0, reward=0, symbol='O',
            movement_strategy=OgreMovementStrategy(), color=7
        )
        self._set_param(health="very_strong", agility="weak",
                        strength="very_strong", hostility="medium")

        self.resting = False  # Флаг отдыха

    def move(self, level, player_x, player_y):
        self.movement_strategy.move(self, level, player_x, player_y)

    def attack(self, player) -> str:
        if self.resting:
            self.resting = False
            return "Ogre is resting and cannot attack!"
        damage = self.damage_calculation()
        attack_result = player.take_damage(damage)
        self.resting = True
        if attack_result == "dodge":
            return f"{player.player_name} dodged!"
        return f"Ogre attacks {player.player_name} for {damage} damage and is now resting!"


class SnakeMage(EnemyFactory):
    """Змей-маг (отображение: белая s): Очень высокая ловкость. Высокая враждебность.
    Ходит по карте по диагонали, постоянно меняя сторону. У каждой успешной атаки есть вероятность «усыпить» игрока на один ход."""

    def __init__(self, lvl_number):
        super().__init__(
            x=0, y=0, lvl_number=lvl_number,
            health=0, agility=0,
            strength=0, hostility=0, reward=0, symbol='s',
            movement_strategy=SnakeMovementStrategy(), color=1
        )
        self._set_param(health="weak", agility="very_strong",
                        strength="medium", hostility="strong")

    def move(self, level, player_x, player_y):
        self.movement_strategy.move(self, level, player_x, player_y)

    def attack(self, player):
        damage = self.damage_calculation()
        attack_result = player.take_damage(damage)
        if attack_result == "dodge":
            return f"{player.player_name} dodged!"
        if random() < 0.3:  # 30% шанс усыпить
            player.sleep_turns = True
            return f"Snake Mage attacks {player.player_name} for {damage} damage and puts {player.player_name} to sleep!"
        return f"Snake Mage attacks {player.player_name} for {damage} damage!"


class Mimik(EnemyFactory):
    """Мимик (белая m), который имитирует предметы. Высокая ловкость, низкая сила, высокое здоровье и низкая враждебность."""

    def __init__(self, lvl_number):
        super().__init__(
            x=0, y=0, lvl_number=lvl_number,
            health=0, agility=0,
            strength=0, hostility=0, reward=0,
            symbol=choice(list(ITEM_TYPES.values())),
            movement_strategy=BasicMovementStrategy(), color=1
        )
        self._set_param(health="strong", agility="strong",
                        strength="weak", hostility="weak")

    def move(self, level, player_x, player_y):
        self.movement_strategy.move(self, level, player_x, player_y)

    def attack(self, player):
        damage = self.damage_calculation()
        attack_result = player.take_damage(damage)
        if attack_result == "dodge":
            return f"{player.player_name} dodged!"
        return f"Mimik attacks {player.player_name} for {damage} damage!"


def create_enemies(lvl_number):
    count = round((MIN_LVL_ENEMIES_NUM + int(lvl_number))
                  * LVL_GEN_COEF["enemies_count"])
    if count > MAX_LVL_ENEMIES_NUM:
        count = MAX_LVL_ENEMIES_NUM
    return [EnemyFactory.create_enemy(lvl_number) for _ in range(count)]
