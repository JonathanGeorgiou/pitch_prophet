# app/models.py

from datetime import datetime, timezone
from sqlalchemy import (
    ForeignKey,
    UniqueConstraint, Integer,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.db import Base
from db.enums import Points


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    short_name: Mapped[str | None] = mapped_column()
    external_id: Mapped[int | None] = mapped_column(unique=True)


class Fixture(Base):
    __tablename__ = "fixtures"

    id: Mapped[int] = mapped_column(primary_key=True)
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    kickoff_time: Mapped[datetime] = mapped_column()
    status: Mapped[str] = mapped_column()  # scheduled | finished
    external_id: Mapped[int | None] = mapped_column(unique=True)

    home_team: Mapped[Team] = relationship("Team", foreign_keys=[home_team_id])
    away_team: Mapped[Team] = relationship("Team", foreign_keys=[away_team_id])
    result: Mapped["Result"] = relationship(back_populates="fixture")
    predictions: Mapped[list["Prediction"]] = relationship(back_populates="fixture")

    def get_prediction_for_player(self, player: Player) -> "Prediction | None":
        return next((p for p in self.predictions if p.player_id == player.id), None)


class Result(Base):
    __tablename__ = "results"

    fixture_id: Mapped[int] = mapped_column(
        ForeignKey("fixtures.id"),
        primary_key=True,
    )
    home_goals: Mapped[int] = mapped_column()
    away_goals: Mapped[int] = mapped_column()
    updated_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    fixture: Mapped["Fixture"] = relationship(back_populates="result")


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    fixture_id: Mapped[int] = mapped_column(ForeignKey("fixtures.id"))
    predicted_home_goals: Mapped[int | None] = mapped_column()
    predicted_away_goals: Mapped[int | None] = mapped_column()
    submitted_time: Mapped[datetime] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("player_id", "fixture_id"),
    )

    player: Mapped[Player] = relationship("Player")
    fixture: Mapped[Fixture] = relationship(back_populates="predictions")

    @hybrid_property
    def predicted(self):
        return (self.predicted_home_goals != None) & (self.predicted_away_goals != None)



class PredictionScore(Base):
    __tablename__ = "prediction_scores"

    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), primary_key=True)
    fixture_id: Mapped[int] = mapped_column(ForeignKey("fixtures.id"), primary_key=True)
    prediction_id: Mapped[int | None] = mapped_column(ForeignKey("predictions.id"))
    points_awarded: Mapped[int] = mapped_column(Integer)
    calculated_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    prediction: Mapped[Prediction | None] = relationship("Prediction", backref="score")
    player: Mapped[Player] = relationship("Player")
    fixture: Mapped[Fixture] = relationship("Fixture")
