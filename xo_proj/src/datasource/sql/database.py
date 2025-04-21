from typing import Annotated
from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from datasource.sql.config import settings

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=False,
)

engine_without_base = create_engine(
    url=settings.DATABASE_URL_without_base(),
    echo=False,
)

session_factory = sessionmaker(bind=sync_engine)

str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }

    repr_cols_num = 30
    repr_cols = tuple()

    def __repr__(self):
        # cols = [f"{k}={getattr(self, k)}" for k in self.__table__.columns.keys()]
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
