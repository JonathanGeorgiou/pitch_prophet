from typing import Sequence

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.schema import Player


class PlayerService:
    def __init__(self, session: Session):
        self._db = session

    def list_players(self) -> Sequence[Player]:
        return self._db.scalars(select(Player)).all()

    def get_player(self, player_id: int) -> Player:
        return self._db.scalars(select(Player).where(Player.id == player_id)).first()

    def create_player(self, name: str) -> Player:
        player = Player(name=name)
        self._db.add(player)
        self._db.commit()
        self._db.refresh(player)
        return player

    def update_player(self, player_id: int, name: str) -> Player | None:
        player = self.get_player(player_id)
        if not player:
            return None
        player.name = name
        self._db.commit()
        self._db.refresh(player)
        return player

    def delete_player(self, player_id: int) -> bool:
        player = self.get_player(player_id)
        if not player:
            return False
        self._db.delete(player)
        self._db.commit()
        return True
