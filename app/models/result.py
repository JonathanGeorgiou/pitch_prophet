from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.fixtures import FixtureRead


class ResultRead(BaseModel):
    fixture: FixtureRead
    home_goals: int
    away_goals: int
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
