# orm.py

from sqlalchemy import text, inspect, func
from sqlalchemy.exc import SQLAlchemyError
from datasource.sql.database import Base, session_factory, sync_engine, engine_without_base
from datasource.sql.model import GameSessionsOrm, UsersOrm


class SyncORM:
    @staticmethod
    def get_database_list():
        with engine_without_base.connect() as conn:
            result = conn.execute(text("SELECT datname FROM pg_database WHERE datistemplate = false"))
            return [row[0] for row in result]

    @staticmethod
    def create_database_if_not_exists(db_name: str = "johnalen"):
        databases = SyncORM.get_database_list()
        if db_name not in databases:
            try:
                with engine_without_base.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
                    # Создаём новую базу данных
                    conn.execute(text(f"CREATE DATABASE {db_name}"))
                    conn.commit()
                    print(f"База данных '{db_name}' успешно создана.")
            except SQLAlchemyError as e:
                print(f"Ошибка при создании базы данных: {e}")
        else:
            print(f"База данных '{db_name}' уже существует.")

    @staticmethod
    def drop_database(db_name: str = "johnalen"):
        try:
            with engine_without_base.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
                # Создаём новую базу данных
                conn.execute(text(f"DROP DATABASE {db_name}"))
                print(f"База данных '{db_name}' успешно удалена.")
                conn.commit()
        except SQLAlchemyError as e:
            print(f"Ошибка при удалении базы данных: {e}")

    @staticmethod
    def create_tables():
        db_name, tables = SyncORM.get_tables()
        if not tables:
            print(f"Таблицы не найдены в базе данных {db_name}. Создаём новые...")
            Base.metadata.create_all(sync_engine)
            print(f"Таблицы успешно созданы")
        else:
            print(f"Таблицы уже существуют в базе данных {db_name}. Пропускаем создание."
                  f"Список таблиц: {tables}")

    @staticmethod
    def drop_tables():
        Base.metadata.drop_all(sync_engine)
        print("Таблицы успешно удалены.")

    @staticmethod
    def get_tables():
        with session_factory() as sess:
            db_name = sess.get_bind().engine.url.database
            inspector = inspect(sess.get_bind())
            tables = inspector.get_table_names()
        return db_name, tables

    @staticmethod
    def upsert_data(game_id, board, player_symbol, player2_symbol,
                    computer_symbol, winner, is_game_over, computer_first_move, user_id,
                    user_login, statement, user2_id, user2_login, multiplayer):
        with session_factory() as sess:
            existing_record = sess.query(GameSessionsOrm).filter_by(game_id=game_id).first()

            if existing_record:
                update_values = {
                    "board": board,
                    "winner": winner,
                    "is_game_over": is_game_over,
                    "computer_first_move": computer_first_move,
                    "statement": statement,
                    "user2_id": user2_id,
                    "user2_login": user2_login
                }

                if winner:
                    ended_at_value = sess.execute(func.timezone('UTC-7', func.now())).scalar()
                    update_values["ended_at"] = ended_at_value
                    created_at_value = existing_record.created_at
                    duration = round((ended_at_value - created_at_value).total_seconds(), 2)
                    update_values["duration_seconds"] = duration
                    print("Победитель и время завершения игры добавлены в базу данных.")

                sess.query(GameSessionsOrm).filter_by(game_id=game_id).update(update_values)
                print("Данные успешно обновлены в базе данных.")
            else:
                new_record = GameSessionsOrm(
                    game_id=game_id,
                    board=board,
                    player_symbol=player_symbol,
                    player2_symbol=player2_symbol,
                    computer_symbol=computer_symbol,
                    winner=winner,
                    is_game_over=is_game_over,
                    computer_first_move=computer_first_move,
                    user_id=user_id,
                    user_login=user_login,
                    statement=statement,
                    user2_id=user2_id,
                    user2_login=user2_login,
                    multiplayer=multiplayer
                )
                sess.add(new_record)
                print("Данные успешно добавлены в базу данных.")

            sess.commit()

    @staticmethod
    def get_data(game_id):
        with session_factory() as sess:
            data = sess.query(GameSessionsOrm).filter_by(game_id=game_id).all()
            return data[0] if data != [] else None

    @staticmethod
    def get_last_active_game(user_id):
        with session_factory() as sess:
            data = (sess.query(GameSessionsOrm)
                    .filter_by(user_id=user_id, is_game_over=False, multiplayer=True)
                    .order_by(GameSessionsOrm.id.desc()).first())
            return data if data else None

    @staticmethod
    def add_user(uid, login, password):
        with session_factory() as sess:
            user = UsersOrm(uid=uid, login=login, password=password)
            sess.add(user)
            sess.commit()

    @staticmethod
    def get_user(login) -> UsersOrm | None:
        with session_factory() as sess:
            user = sess.query(UsersOrm).filter_by(login=login).first()
            return user
    @staticmethod
    def get_user_by_uid(uid) -> UsersOrm | None:
        with session_factory() as sess:
            user = sess.query(UsersOrm).filter_by(uid=uid).first()
            return user

    @staticmethod
    def get_all_games_single(user_id):
        with session_factory() as sess:
            games = sess.query(GameSessionsOrm).filter_by(user_id=user_id, multiplayer=False).order_by(
                GameSessionsOrm.created_at.desc()).all()
            return games

    @staticmethod
    def get_all_games_multi():
        with session_factory() as sess:
            games = sess.query(GameSessionsOrm).filter_by(multiplayer=True).order_by(
                GameSessionsOrm.created_at.desc()).all()
            return games
