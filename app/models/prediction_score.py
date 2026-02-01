from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.fixtures import FixtureRead
from app.models.player import PlayerRead
from app.models.prediction import PredictionRead


class PredictionScoreRead(BaseModel):
    player: PlayerRead
    fixture: FixtureRead
    prediction: PredictionRead
    points_awarded: int
    calculated_at: datetime

    model_config = ConfigDict(from_attributes=True)
