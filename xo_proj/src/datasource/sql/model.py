from typing import Annotated
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from datasource.sql.database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('UTC-7', NOW())"))]
updated_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('UTC-7', NOW())")
                                               , onupdate=text("TIMEZONE('UTC-7', NOW())"))]


class UsersOrm(Base):
    __tablename__ = "users"
    id: Mapped[intpk]
    uid: Mapped[str]
    login: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    games: Mapped[list["GameSessionsOrm"]] = relationship(back_populates="user")


class GameSessionsOrm(Base):
    __tablename__ = "game_sessions"
    id: Mapped[intpk]
    game_id: Mapped[str]
    board: Mapped[str]
    player_symbol: Mapped[str]
    computer_symbol: Mapped[str | None]
    winner: Mapped[str | None]
    duration_seconds: Mapped[float | None]
    statement: Mapped[str]
    computer_first_move: Mapped[bool | None]
    is_game_over: Mapped[bool]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["UsersOrm"] = relationship(back_populates="games")
    user_login: Mapped[str]
    multiplayer: Mapped[bool] = mapped_column(default=False)
    player2_symbol: Mapped[str | None]
    user2_id: Mapped[int | None]
    user2_login: Mapped[str | None]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    ended_at: Mapped[datetime | None]