from datasource.sql.orm import SyncORM


class SQLService:

    @staticmethod
    def run():
        # SyncORM.drop_tables()
        SyncORM.create_tables()
