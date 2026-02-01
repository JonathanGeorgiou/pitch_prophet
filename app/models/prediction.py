from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.fixtures import FixtureRead
from app.models.player import PlayerRead

class PredictionBase(BaseModel):
    player: PlayerRead
    fixture: FixtureRead
    predicted_home_goals: int
    predicted_away_goals: int

class PredictionCreate(PredictionBase):
    pass

class PredictionRead(BaseModel):
    id: int
    player: PlayerRead
    fixture: FixtureRead
    predicted_home_goals: int
    predicted_away_goals: int
    submitted_time: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)