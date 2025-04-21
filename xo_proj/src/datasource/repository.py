from datasource.mapper import DatasourceMapper
from domain.model import GameSession, User


class UserRepository:
    @staticmethod
    def add_user(uid: str, login: str, password: str) -> None:
        """Добавляет пользователя в базу данных."""
        DatasourceMapper.add_user_to_sql(uid=uid, login=login, password=password)

    @staticmethod
    def get_user(login: str) -> User | None:
        return DatasourceMapper.get_user_from_sql(login)


class GameRepository:
    @staticmethod
    def save_game(session: GameSession) -> None:
        """Сохраняет игровую сессию в базу данных."""
        DatasourceMapper.to_sql_storage(session)


    @staticmethod
    def get_game(session_id: str) -> GameSession:
        """Возвращает игровую сессию по её ID."""
        return DatasourceMapper.from_sql_storage(session_id)

    @staticmethod
    def get_last_active_game(user_id: int) -> GameSession:
        """Возвращает игровую сессию по её ID."""
        return DatasourceMapper.get_last_active_game_from_sql_storage(user_id)


    @staticmethod
    def get_all_games_single(user_id) -> list[GameSession]:
        return DatasourceMapper.get_all_games_single(user_id)

    @staticmethod
    def get_all_games_multi() -> list[GameSession]:
        return DatasourceMapper.get_all_games_multi()
