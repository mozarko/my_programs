from typing import Optional
from random import randint

from constants.game_constants import *
from logic.movement_strategies import PlayerMovementStrategy
from logic.item import Item
from datalayer.stats import Stats


class Character:

    def __init__(self, player_name: str, x: int = 0, y: int = 0,
                 movement_strategy=PlayerMovementStrategy(),
                 cur_hp: int = 150,
                 max_hp: int = 150,
                 agility: int = 15,
                 strength: int = 20,
                 bonus_max_hp: int = 0,
                 bonus_agility: int = 0,
                 bonus_strength: int = 0
                 ):
        self.symb = '@'
        self.x = x
        self.y = y
        self.max_hp = max_hp
        self.cur_hp = cur_hp
        self.agility = agility
        self.strength = strength
        self.bonus_agility = bonus_agility
        self.bonus_strength = bonus_strength
        self.bonus_max_hp = bonus_max_hp
        self.movement_strategy = movement_strategy
        self.backpack = Backpack()
        self.equipped_weapon = None
        self.sleep_turns = False
        self.player_name = player_name
        self.active_buffs = []
        self.stats = Stats()

    def move(self, level, direction):
        if self.movement_strategy:
            self.movement_strategy.move(self, level, direction)

    def pick_up_item(self, item) -> bool:
        if self.backpack.take_item(item):
            return True
        return False

    def drop_sword(self):
        if self.equipped_weapon is not None:
            self.equipped_weapon.x = self.x + 1
            self.equipped_weapon.y = self.y
            dropped_sword = self.equipped_weapon
            self.bonus_strength -= dropped_sword.strength
            self.equipped_weapon = None
            return dropped_sword
        return None

    def get_items_by_type(self, item_type: str) -> list[Item]:
        return [item for item in self.backpack.items_list if item.item_type == item_type]

    def equip_sword(self, swords: list[Item], idx: int) -> tuple[str, Optional[Item]]:
        dropped_sword = self.drop_sword()
        sword = swords[idx]
        self.equipped_weapon = sword
        self.bonus_strength += sword.strength
        self.backpack.remove_item(sword)
        return f"{self.player_name} equipped a {sword.item_subtype} {sword.item_type}. Strength increased by {sword.strength}", dropped_sword

    def use_scroll(self, scrolls: list[Item], idx: int):
        scroll = scrolls[idx]
        if scroll.target_stat == 'agility':
            self.agility += scroll.agility
            value = scroll.agility
        elif scroll.target_stat == 'strength':
            self.strength += scrolls[idx].strength
            value = scroll.strength
        elif scroll.target_stat == 'max_hp':
            self.max_hp += scroll.max_hp
            self.cur_hp += scroll.max_hp
            value = scroll.max_hp
        self.backpack.remove_item(scrolls[idx])
        self.stats.used_scrolls += 1
        return f"{self.player_name} reads a {scroll.item_subtype} {scroll.item_type} and raises {scroll.target_stat} by {value}"

    def eat_food(self, foods: list[Item], idx: int):
        if self.cur_hp == self.max_hp:
            self.max_hp += 10 * RARITY_MODIFIERS[foods[idx].item_subtype]
            self.cur_hp = self.max_hp
        else:
            self.cur_hp = min(
                self.cur_hp + foods[idx].heal_hp, self.max_hp)
        self.backpack.remove_item(foods[idx])
        self.stats.eaten_food += 1
        return f"{self.player_name} ate the {foods[idx].item_subtype} {foods[idx].item_type} and healed {foods[idx].heal_hp} hp"

    def use_elixir(self, elixirs: list[Item], idx: int):
        elix = elixirs[idx]
        target = elixirs[idx].target_stat
        if target == 'agility':
            self.bonus_agility += elix.agility
            value = elix.agility
        elif target == 'strength':
            self.bonus_strength += elix.strength
            value = elix.strength
        elif target == 'max_hp':
            self.max_hp += elix.max_hp
            self.cur_hp += elix.max_hp
            value = elix.max_hp

        self.active_buffs.append({
            'stat': target,
            'value': value,
            'expire_at': BUFF_DUR
        })

        self.backpack.remove_item(elix)
        self.stats.used_elixir += 1
        return f"{self.player_name} drinks a {elix.item_subtype} {elix.item_type} and temporarily increases his {target} by {value}"

    def remove_buff(self):
        for buff in self.active_buffs[:]:
            if buff['expire_at'] == 0:
                if buff['stat'] == 'agility':
                    self.bonus_agility -= buff['value']
                elif buff['stat'] == 'strength':
                    self.bonus_strength -= buff['value']
                elif buff['stat'] == 'max_hp':
                    self.max_hp -= buff['value']
                self.active_buffs.remove(buff)
            else:
                buff['expire_at'] -= 1

    def get_total_strength(self) -> int:
        """Калькуляция общей силы игрока"""
        return self.strength + self.bonus_strength

    def calculate_dodge_chance(self):
        dodge_chance = self.agility * DODGE_COEFFICIENT
        return min(dodge_chance, MAX_DODGE_CHANCE)

    def attack(self, enemy) -> str:
        """Атака игрока"""
        if self.sleep_turns:
            self.sleep_turns = False
            return f"{self.player_name} can't attack, he's asleep."
        damage = self.get_total_strength() + randint(-5, 5)
        attack_result = enemy.take_damage(damage)

        if attack_result == "dodge_first_attack":
            enemy.dodge_first_attack = False
            return f"{self.player_name} attacks {enemy.__class__.__name__}, but {enemy.__class__.__name__} dodged!"

        if attack_result == "dodge":
            return f"{enemy.__class__.__name__} dodged!"

        self.stats.hits_dealt += 1
        return f"{self.player_name} attacks {enemy.__class__.__name__} for {damage} damage!"

    def take_damage(self, damage: int):
        if randint(0, 100) <= self.calculate_dodge_chance():
            return "dodge"
        self.cur_hp -= damage
        self.stats.hits_taken += 1
        return "ok"

    def is_dead(self):
        return self.cur_hp <= 0


class Backpack:
    def __init__(self):
        self.items_list: list[Item] = []
        self.max_space = BACKPACK_MAX_SIZE

    def take_item(self, item) -> bool:
        if len(self.items_list) < self.max_space:
            self.items_list.append(item)
            return True
        return False

    def remove_item(self, item) -> bool:
        if item in self.items_list:
            self.items_list.remove(item)
            return True
        return False

    def __str__(self):
        return f"Backpack({len(self.items_list)}/{self.max_space}): {self.items_list}"
