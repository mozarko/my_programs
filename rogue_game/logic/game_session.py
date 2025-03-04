import random

from constants.game_constants import *
from logic.character import Character
from logic.enemy_factory import create_enemies
from logic.item import Item
from logic.level import Level
from logic.autoleveling import AutoLeveling


class GameSession:
    def __init__(self, player_name: str, is_3d: bool = False):
        self.player_name = player_name if player_name != "" else "Player"
        self.enemies = []
        self.items = []
        self.level = None
        self.level_num = 0
        self.player = Character(player_name=player_name) if self.player_name != 'mayweath' else Character(
            player_name=player_name,
            cur_hp=999, max_hp=999, strength=999, agility=999)
        self.message_bar = f"Goodluck, {self.player_name}!"
        self.in_combat = False  # Флаг, указывающий, что игрок в бою
        self.current_enemy = None  # Текущий враг, с которым идет бой
        self.is_3d = is_3d
        self.autolvl = AutoLeveling(len(self.enemies), len(
            self.items), self.enemies, self.player)

    def is_exit_door(self) -> bool:
        if self.level.compelete_lvl(self.player):
            self.autolvl.end_calculate_difficulty_coefficients()
            self.autolvl.reset_counters()
            return True
        return False

    def create_new_level(self):
        self.level = Level()
        self.level_num += 1
        self.enemies = create_enemies(self.level_num)
        self.items = Item.create_items_list(
            random.randint(MIN_ITEM_ON_MAP_EXCEPT_SWORD_AND_FOOD + int(LVL_GEN_COEF["items_count"]),
                           MAX_ITEM_ON_MAP_EXCEPT_SWORD_AND_FOOD + int(LVL_GEN_COEF["items_count"])), self.level_num)
        self.level.create_lvl(self.player, self.enemies, self.items)
        self.autolvl = AutoLeveling(len(self.enemies), len(
            self.items), self.enemies, self.player)
        self.autolvl.start_calculate_difficulty_coefficients()

    def check_item_pickup(self) -> bool:
        for item in self.items[:]:
            if item.is_player_close(self.player.x, self.player.y):
                if item.item_type == 'treasure':
                    self.player.stats.gold += item.gold
                    self.message_bar = f'{self.player_name} picked up {item.item_subtype} {item.item_type} (Gold: +{item.gold})'
                    self.items.remove(item)
                elif self.player.pick_up_item(item):
                    self.message_bar = f'{self.player_name} take a {item.item_subtype} {item.item_type}'
                    self.items.remove(item)
                return True
        return self.pickup_key()

    def pickup_key(self) -> bool:
        for key in self.level.keys.values():
            if [self.player.x, self.player.y] == key.coordinates:
                key_color = ''
                match key.color_idx:
                    case 2:
                        key_color = 'purple'
                    case 3:
                        key_color = 'red'
                    case 7:
                        key_color = 'yellow'
                self.message_bar = f'{self.player_name} picked up a {key_color} key'
                self.level.keys.pop(key.color_idx)
                self.level.open_door(key.color_idx)
                return True
        return False

    def enemies_step(self):
        for enemy in self.enemies:
            if hasattr(enemy, "invisible"):
                enemy.check_invisible()
            enemy.move(self.level,
                       self.player.x, self.player.y)

    def check_for_combat(self) -> bool:
        """
        Проверяет, находится ли игрок рядом с врагом.
        Если да, то да начнется бой!
        """
        for enemy in self.enemies:
            if abs(self.player.x - enemy.x) <= 1 and abs(self.player.y - enemy.y) <= 1:
                self.in_combat = True
                self.current_enemy = enemy
                if hasattr(self.current_enemy, "invisible"):
                    self.current_enemy.invisible = False
                    self.current_enemy.set_symb()
                if self.player.x == enemy.x and self.player.y == enemy.y:
                    if not self.level.is_blocked(enemy.x + 1, enemy.y):
                        enemy.x += 1
                    elif not self.level.is_blocked(enemy.x - 1, enemy.y):
                        enemy.x -= 1
                    elif not self.level.is_blocked(enemy.x, enemy.y - 1):
                        enemy.y -= 1
                    elif not self.level.is_blocked(enemy.x, enemy.y + 1):
                        enemy.y += 1
                self.message_bar = f"{self.player_name} started combat with {enemy.__class__.__name__}! Press SPACE to attack"
                return True
        return False

    def combat_turn(self) -> bool:
        """Обрабатывает ход боя."""
        if not self.in_combat or not self.current_enemy:
            return False

        player_attack_result = self.player.attack(self.current_enemy)
        self.autolvl.hits_dealt += 1
        self.message_bar = (player_attack_result +
                            f" {self.current_enemy.__class__.__name__} "
                            f"HP: {self.current_enemy.cur_hp}/{self.current_enemy.max_hp}")

        if self.current_enemy.is_dead():
            self.player.stats.gold += self.current_enemy.reward
            self.message_bar = (f"{self.current_enemy.__class__.__name__} is defeated! {self.player.player_name}"
                                f" get {self.current_enemy.reward} gold")
            self.enemies.remove(self.current_enemy)
            self.in_combat = False
            self.current_enemy = None
            self.autolvl.enemies_defeated += 1
            self.player.stats.enemies_defeated += 1
            return False

        enemy_attack_result = self.current_enemy.attack(self.player)
        self.autolvl.hits_taken += 1
        self.message_bar += f"\n{enemy_attack_result} Press SPACE to attack"

        if self.player.is_dead():
            self.in_combat = False
            self.current_enemy = None
            return False

        return True
