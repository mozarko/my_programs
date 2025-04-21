import json
from constants.game_constants import *
from logic.game_session import *
from logic.enemy_factory import *
from logic.character import *
from logic.level import *

class Loading:
    def __item_deserialization(data: dict) -> Item:
        """
        Десериализует предмет

        Args:
            data (dict): десериализуемые данные предмета

        Returns:
            Item: десериализованный объект предмета
        """
        item = Item(data["item_type"], data["item_subtype"], data["symbol"], data["heal_hp"], 
                        data["max_hp"], data["agility"], data["strength"], data["target_stat"], data["gold"])
        item.x = data["x"]
        item.y = data["y"]
        
        return item
        
    def __items_deserialization(data: list[dict]) -> list[Item]:
        """
        Десериализует список предметов

        Args:
            data (list[dict]): десериализуемые данные списка предметов
        Returns:
            list[Item]: десериализованный список предметов
        """
        items = []
        for i in data:
            items.append(Loading.__item_deserialization(i))
            
        return items    
            
    def __equipped_weapon_deserialization(data: dict) -> Item:
        """
        Десериализует данные выбранного игроком оружия

        Args:
            data (dict): десериализуемые данные выбранного игроком оружия

        Returns:
            Item: десериализованный объект выбранного игроком оружия
        """
        if data is not None:
            return Loading.__item_deserialization(data)
        else:
            return None
    
    def __stats_deserialization(stats: Stats, data: dict):
        """
        Десериализует данные статистики игрока

        Args:
            stats (Stats): объект статистики игрока для записи сериализованных данных
            data (dict): десериализуемые данные статистики игрока
        """
        stats.gold = data["gold"]
        stats.eaten_food = data["eaten_food"]
        stats.used_elixir = data["used_elixir"]
        stats.used_scrolls = data["used_scrolls"]
        stats.enemies_defeated = data["enemies_defeated"]
        stats.hits_dealt = data["hits_dealt"]
        stats.hits_taken = data["hits_taken"]
        stats.tiles_walked = data["tiles_walked"]
    
    def __character_deserialization(player: Character, data: dict):
        """
        Десериализует данные игрока

        Args:
            player (Character): объект игрока для записи сериализованных данных
            data (dict): десериализуемые данные игрока
        """
        player.symb = data["symb"]
        player.x = data["x"]
        player.y = data["y"]
        player.max_hp = data["max_hp"]
        player.cur_hp = data["cur_hp"]
        player.agility = data["agility"]
        player.strength = data["strength"]
        player.bonus_agility = data["bonus_agility"]
        player.bonus_strength = data["bonus_strength"]
        player.bonus_max_hp = data["bonus_max_hp"]
        player.backpack.items_list = Loading.__items_deserialization(data["backpack"])
        player.equipped_weapon = Loading.__equipped_weapon_deserialization(data["equipped_weapon"])
        player.sleep_turns = data["sleep_turns"]
        player.active_buffs = data["active_buffs"]   
        Loading.__stats_deserialization(player.stats, data["stats"])
    
    def __enemy_deserialization(enemy: EnemyFactory, data: dict):
        """
        Десериализует данные врага

        Args:
            enemy (EnemyFactory): объект врага для записи сериализованных данных
            data (dict): десериализуемые данные врага
        """
        enemy.x = data["x"]
        enemy.y = data["y"]
        enemy.cur_hp = data["cur_hp"]
        enemy.max_hp = data["max_hp"]
        enemy.agility = data["agility"]
        enemy.strength = data["strength"]
        enemy.hostility = data["hostility"]
        enemy.reward = data["reward"]
        
    def __enemies_deserialization(enemies: list[EnemyFactory], datas: list[dict]):
        """
        Десериализует данные врагов уровня игровой сессии

        Args:
            enemies (list[EnemyFactory]): список объектов врагов 
                для записи сериализованных данных
            datas (list[dict]): десериализуемые данные врагов
        """
        for data in datas:
            enemy = None
            match data["symbol"]:
                case "z": 
                    enemy = Zombie(data["lvl_number"])
                case "v": 
                    enemy = Vampire(data["lvl_number"])
                    enemy.dodge_first_attack = data["dodge_first_attack"]
                case "g":
                    enemy = Ghost(data["lvl_number"])
                    enemy.invisible = data["invisible"]
                case "O":
                    enemy = Ogre(data["lvl_number"])
                    enemy.resting = data["resting"]
                case "s":
                    enemy = SnakeMage(data["lvl_number"])
                case _:
                    enemy = Mimik(data["lvl_number"])
                    
            Loading.__enemy_deserialization(enemy, data)
            enemies.append(enemy)
            
    
    def __tiles_deserialization(datas: list[list[dict]]) -> list[list[Tile]]:
        """
        Десериализует данные блоков игрового поля

        Args:
            datas (list[list[dict]]): десериализуемые данные блоков игрового поля

        Returns:
            list[list[Tile]]: двумерный массив блоков игрового поля
        """
        tiles = []
        for data in datas:
            block = []
            for tile in data:
                block.append(Tile(tile["blocked"], tile["block_sight"]))
            tiles.append(block)
        
        return tiles
    
    def __rooms_deserialization(datas: list[dict]) -> list[Room]:
        """
        Десериализует данные комнат

        Args:
            datas (list): десериализуемые данные комнат

        Returns:
            list: список комнат
        """
        rooms = []
        for data in datas:
            room = Room(1,1,1,1,1)
            room.x1 = data["x1"]
            room.y1 = data["y1"]
            room.x2 = data["x2"]
            room.y2 = data["y2"]
            room.room_number = data["room_number"]
            rooms.append(room)
        
        return rooms
        
    def __corridors_deserialization(datas: list) -> list[Corridor]:
        """
        Десериализует данные корридоров

        Args:
            datas (list): десериализуемые данные корридоров

        Returns:
            list: список корридоров
        """
        corridors = []
        for data in datas:
            corridor = Corridor()
            corridor.rooms = Loading.__rooms_deserialization(data["rooms"])
            corridor.coordinates = data["coordinates"]
            corridor.color_idx = data["color_idx"]
            corridors.append(corridor)

        return corridors
        
    def __doors_deserialization(datas: list) -> dict[int: Room]:
        """
        Десериализует данные дверей

        Args:
            datas (list): десериализуемые данные дверей

        Returns:
            dict: словарь дверей в виде {индекс цвета двери: объект двери}
        """
        doors = {}
        for data in datas:
            corridors = Loading.__corridors_deserialization([data["corridor"]])
            door = Door(data["color_idx"], corridors)
            doors.update({door.color_idx: door})
        return doors
    
    def __keys_deserialization(datas: list) -> dict:
        """
        Десериализует данные ключей

        Args:
            datas (list): десериализуемые данные ключей

        Returns:
            dict: словарь ключей в виде {индекс цвета ключа: объект ключа}
        """
        keys = {}
        for data in datas:
            key = Key(data["color_idx"], Loading.__rooms_deserialization([data["room"]]))
            key.symb = data["symb"]
            key.coordinates = data["coordinates"]
            keys.update({key.color_idx: key})
        return keys
        
    def __level_deserialization(data: dict) -> Level:
        """
        Десериализует данные уровня игровой сессии

        Args:
            data (dict): десериализуемые данные уровня игровой сессии

        Returns:
            Level: объект уровня игровой сессии
        """
        level = Level()
        level.tiles = Loading.__tiles_deserialization(data["tiles"])
        level.exit_door_x = data["exit_door_x"]
        level.exit_door_y = data["exit_door_y"]
        level.rooms = Loading.__rooms_deserialization(data["rooms"])
        level.corridors = Loading.__corridors_deserialization(data["corridors"])
        level.maze_path = data["maze_path"]
        level.doors = Loading.__doors_deserialization(data["doors"])
        level.keys = Loading.__keys_deserialization(data["keys"])
        
        return level
        
    @staticmethod
    def load_game() -> GameSession:
        """
        Десериализует данные игровой сессию из файла сохранения формата JSON

        Returns:
            GameSession: объект игровой сессии
        """
        with open(SAVE_FILE_PATH, "r") as file:
            data = json.load(file)
            game_session = GameSession(data["player"]["player_name"])
            Loading.__character_deserialization(game_session.player, data["player"])
            Loading.__enemies_deserialization(game_session.enemies, data["enemies"])
            game_session.items = Loading.__items_deserialization(data["items"])
            game_session.level_num = data["level_num"]
            game_session.level = Loading.__level_deserialization(data["level"])
            
        return game_session
