from domain.model import GameSession, GameBoard, User, State, Statements, GameState
from datasource.sql.orm import SyncORM


class DatasourceMapper:
    @staticmethod
    def add_user_to_sql(uid: str, login: str, password: str):
        SyncORM.add_user(uid=uid, login=login, password=password)

    @staticmethod
    def get_user_from_sql(login: str = None, uid: str = None) -> User | None:
        if login:
            user_from_sql = SyncORM.get_user(login)
        elif uid:
            user_from_sql = SyncORM.get_user_by_uid(uid)
        else:
            raise Exception("No login or uid provided")

        if not user_from_sql:
            raise Exception("User not found")

        return User(user_id=user_from_sql.id, uid=user_from_sql.uid, login=user_from_sql.login,
                    password=user_from_sql.password) if user_from_sql else None

    @staticmethod
    def to_sql_storage(domain_session: GameSession):
        SyncORM.upsert_data(game_id=str(domain_session.get_game_id()),
                            board=(" | ".join(
                                ", ".join(map(str, sublist)) for sublist in domain_session.get_board().get_board())),
                            player_symbol=domain_session.get_player_symbol(),
                            player2_symbol=domain_session.player2_symbol,
                            computer_symbol=domain_session.get_computer_symbol(),
                            winner=domain_session.get_winner(),
                            is_game_over=domain_session.is_game_over,
                            computer_first_move=domain_session.computer_first_move,
                            user_id=domain_session.user_id,
                            user_login=domain_session.user_login,
                            statement=domain_session.current_state.get_current_state(),
                            user2_id=domain_session.user2_id,
                            user2_login=domain_session.user2_login,
                            multiplayer=domain_session.multiplayer
                            )

    @staticmethod
    def get_all_games_single(user_id):
        return DatasourceMapper.all_games_from_sql_storage(SyncORM.get_all_games_single(user_id))

    @staticmethod
    def get_all_games_multi():
        return DatasourceMapper.all_games_from_sql_storage(SyncORM.get_all_games_multi())

    @staticmethod
    def all_games_from_sql_storage(all_games):
        return [DatasourceMapper.to_domain_sess_from_sql_obj(game) for game in all_games]

    @staticmethod
    def from_sql_storage(game_id):
        sql_obj = SyncORM.get_data(str(game_id))
        if sql_obj:
            return DatasourceMapper.to_domain_sess_from_sql_obj(sql_obj)
        else:
            print("Datasource.mapper - Game.id not found")

    @staticmethod
    def get_last_active_game_from_sql_storage(user_id):
        sql_obj = SyncORM.get_last_active_game(user_id)
        if sql_obj:
            return DatasourceMapper.to_domain_sess_from_sql_obj(sql_obj)
        else:
            print("Datasource.mapper - No active game found")

    @staticmethod
    def to_domain_sess_from_sql_obj(sql_obj):
        # Парсим статус и логин из строки, например: "move_player comp2"
        raw_state = sql_obj.statement  # строка из базы
        parts = raw_state.split(" ", 1)  # делим только по первому пробелу
        status_str = parts[0]
        user_login = parts[1] if len(parts) > 1 else None
        state = Statements()
        state.current_state = State(GameState(status_str), user_login)
        return GameSession(game_id=sql_obj.game_id,
                           board=GameBoard([[int(item) for item in sublist.split(", ")] for sublist in
                                            sql_obj.board.split(" | ")]),
                           player_symbol=sql_obj.player_symbol,
                           player2_symbol=sql_obj.player2_symbol,
                           computer_symbol=sql_obj.computer_symbol,
                           computer_first_move=sql_obj.computer_first_move,
                           is_game_over=sql_obj.is_game_over,
                           winner=sql_obj.winner,
                           user_id=sql_obj.user_id,
                           user_login=sql_obj.user_login,
                           user2_id=sql_obj.user2_id,
                           user2_login=sql_obj.user2_login,
                           multiplayer=sql_obj.multiplayer,
                           current_state=state
                           )
