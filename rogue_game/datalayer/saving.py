import json
from constants.game_constants import *
from logic.game_session import *
from logic.enemy_factory import *
from logic.character import *
from logic.level import *

class Saving:
    
    def __objs_serialization(objs: list) -> list[dict]:
        """
        Вспомогательный метод для сериализации "простых" и похожих объектов

        Args:
            objs (list): список сериализуемых объектов

        Returns:
            list[dict]: список сериализованных объектов
        """
        result = []
        for i in objs:
            result.append(i.__dict__)
        
        return result
            
    def __enemies_serialization(enemies: list[EnemyFactory]) -> list[dict]:
        """
        Сериализует врагов

        Args:
            enemies (list[EnemyFactory]): сериализуемый список врагов

        Returns:
            list[dict]: список сериализованных данных врагов
        """
        result = []
        for i in enemies:
            attr = i.__dict__
            attr_copy = attr.copy()
            del attr_copy["movement_strategy"]
            result.append(attr_copy)
        
        return result
    
    def __player_serialization(player: Character) -> dict:
        """
        Сериализует данные об игроке

        Args:
            player (Character): Сериализуемый объект игрока

        Returns:
            dict: сериализованные данные игрока
        """
        attr  = player.__dict__
        attr_copy = attr.copy()
        del attr_copy["movement_strategy"]
        if player.equipped_weapon:
            attr_copy["equipped_weapon"] = player.equipped_weapon.__dict__
        attr_copy["backpack"] = Saving.__objs_serialization(player.backpack.items_list)
        attr_copy["stats"] = player.stats.__dict__
        
        return attr_copy
    
    def __tiles_serialization(tiles: list[list[Tile]]) -> list[list]:
        """
        Сериализует блоки игрового поля

        Args:
            tiles (list[list[Tile]]): Сериализуемые блоки игрового поля

        Returns:
            list[list]: Сериализованные блоки игрового поля
        """
        result = []
        for tile in tiles:
            tmp_list = []
            for i in tile:
                tmp_list.append(i.__dict__)
            result.append(tmp_list) 
        
        return result
    
    def __corridors_serialization(corridors: list[Corridor]) -> list[dict]:
        """
        Сериализует список корридоров

        Args:
            corridors (list[Corridor]): сериализуемый список корридоров

        Returns:
            list: список сериализованных данных корридоров
        """
        result = []
        for corridor in corridors:
            attr = {} 
            attr["rooms"] = Saving.__objs_serialization(corridor.rooms)
            attr["coordinates"] = corridor.coordinates
            attr["color_idx"] = corridor.color_idx
            result.append(attr)
            
        return result
    
    def __door_serialization(data: Door) -> dict:
        """
        Сериализует дверь

        Args:
            data (Door): сериализуемая дверь

        Returns:
            dict: сериализованные данные двери
        """
        corr = Saving.__corridors_serialization([data.corridor])
        return {"color_idx": data.color_idx, 
                "corridor": corr.pop()}
        
    def __doors_serialization(datas: dict) -> list:
        """
        Сериализует список дверей

        Args:
            datas (dict): сериализуемый словрарь дверей типа 
                {цветовой индекс двери: объект двери}

        Returns:
            list: список сериализованных данных дверей
        """
        doors = []
        for value in datas.values():
            doors.append(Saving.__door_serialization(value))    
        return doors
    
    def __key_serialization(data: Key) -> dict:
        """
        Сериализует ключ

        Args:
            data (Key): сериализуемый ключ

        Returns:
            dict: сериализованные данные ключа
        """
        room = Saving.__objs_serialization([data.room])
        return {"symb": data.symb, "color_idx": data.color_idx,
                "room": room.pop(),
                "coordinates": data.coordinates}
    
    def __keys_serialization(datas: dict) -> list:
        """
        Сериализует список ключей

        Args:
            datas (dict): сериализуемый словрарь ключей типа 
                {цветовой индекс ключа: объект ключа}

        Returns:
            list: список сериализованных данных ключей
        """
        keys = []
        for value in datas.values():
            keys.append(Saving.__key_serialization(value))
        return keys
    
    def __level_serialization(level: Level) -> dict:
        """
        Сериализует данные текущего уровня игровой сессии

        Args:
            level (Level): сериализуемый уровень

        Returns:
            dict: сериализованные данные уровня
        """
        attr = {}
        attr["tiles"] = Saving.__tiles_serialization(level.tiles)
        attr["exit_door_x"] = level.exit_door_x 
        attr["exit_door_y"] = level.exit_door_y
        attr["rooms"] = Saving.__objs_serialization(level.rooms)  
        attr["corridors"] = Saving.__corridors_serialization(level.corridors)
        attr["maze_path"] = level.maze_path
        attr["doors"] = Saving.__doors_serialization(level.doors)
        attr["keys"] = Saving.__keys_serialization(level.keys)
        
        return attr
    
    @staticmethod
    def save_game(game_session: GameSession):
        """
        Сохраняет данные игровой сессии в файл формата JSON

        Args:
            game_session (GameSession): сохраняемая игровая сессия
        """
        data = {}
        data["player"] = Saving.__player_serialization(game_session.player)
        data["enemies"] = Saving.__enemies_serialization(game_session.enemies)
        data["items"] = Saving.__objs_serialization(game_session.items)
        data["level_num"] = game_session.level_num
        data["level"] = Saving.__level_serialization(game_session.level)
            
        with open(SAVE_FILE_PATH, "w") as file:
            json.dump(data, file, indent=4)     
        
        