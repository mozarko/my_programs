from __future__ import annotations
import random

from constants.game_constants import *


class Item:
    def __init__(self,
                 item_type: str, item_subtype: str,
                 symbol: str,
                 heal_hp: int = 0, max_hp: int = 0,
                 agility: int = 0, strength: int = 0, target_stat: str = None,
                 gold: int = 0):
        self.x = 0
        self.y = 0
        self.item_type = item_type
        self.item_subtype = item_subtype
        self.symbol = symbol
        self.heal_hp = heal_hp
        self.max_hp = max_hp
        self.agility = agility
        self.strength = strength
        self.target_stat = target_stat  # для свитков или эликсиров
        self.gold = gold

    def __repr__(self):
        return f"{self.item_subtype} {self.item_type}"

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def create_item(item_type: str, item_subtype: str, lvl_number: int) -> Item:
        modifier = RARITY_MODIFIERS[item_subtype]
        symbol = ITEM_TYPES[item_type]

        if item_type == "treasure":
            return Item(item_type, item_subtype, symbol, gold=int(20 * modifier * (1 + 0.1 * (lvl_number - 1))))
        elif item_type == "food":
            return Item(item_type, item_subtype, symbol,
                        heal_hp=int(10 * modifier * (1 + 0.5 * (lvl_number - 1))))
        elif item_type == "elixir":
            chosen_stat = random.choice(["strength", "agility", "max_hp"])
            if chosen_stat == "max_hp":
                return Item(item_type, item_subtype, symbol, target_stat=chosen_stat,
                            **{chosen_stat: int(20 * modifier * (1 + 0.2 * (lvl_number - 1)))})
            else:
                return Item(item_type, item_subtype, symbol, target_stat=chosen_stat,
                            **{chosen_stat: int(10 * modifier * (1 + 0.2 * (lvl_number - 1)))})
        elif item_type == "scroll":
            chosen_stat = random.choice(["strength", "agility", "max_hp"])
            if chosen_stat == "max_hp":
                return Item(item_type, item_subtype, symbol, target_stat=chosen_stat,
                            **{chosen_stat: int(10 * modifier * (1 + 0.1 * (lvl_number - 1)))})
            else:
                return Item(item_type, item_subtype, symbol, target_stat=chosen_stat,
                            **{chosen_stat: int(5 * modifier * (1 + 0.1 * (lvl_number - 1)))})
        elif item_type == "sword":
            return Item(item_type, item_subtype, symbol, strength=int(5 * modifier * (1 + 0.1 * (lvl_number - 1))))

    @staticmethod
    def create_items_list(count: int, lvl_number: int) -> list[Item]:
        items = []
        rarity_keys = list(RARITY_PROBABILITIES.keys())
        rarity_weights = list(RARITY_PROBABILITIES.values())

        # Исключаем еду и меч
        filtered_item_types = {k: v for k, v in ITEM_TYPES.items() if k not in [
            "food", "sword"]}

        for _ in range(random.randint(MIN_FOOD_ON_MAP + int(LVL_GEN_COEF["items_healing"]), MAX_FOOD_ON_MAP)):
            item_subtype = random.choices(
                rarity_keys, weights=rarity_weights, k=1)[0]
            items.append(Item.create_item("food", item_subtype, lvl_number))

        # добавляем на карту только 1 меч с 80% вероятностью
        for _ in range(1):
            if random.random() < 0.8:
                item_subtype = random.choices(
                    rarity_keys, weights=rarity_weights, k=1)[0]
                items.append(Item.create_item(
                    "sword", item_subtype, lvl_number))

        for _ in range(count):
            item_type = random.choice(list(filtered_item_types.keys()))

            item_subtype = random.choices(
                rarity_keys, weights=rarity_weights, k=1)[0]

            items.append(Item.create_item(item_type, item_subtype, lvl_number))
        return items

    def is_player_close(self, player_x: int, player_y: int) -> bool:
        return self.x == player_x and self.y == player_y
