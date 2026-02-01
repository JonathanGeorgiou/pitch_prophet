from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.team import TeamRead


class FixtureBase(BaseModel):
    kickoff_time: datetime
    status: str

class FixtureRead(FixtureBase):
    id: int
    home_team: TeamRead
    away_team: TeamRead

    model_config = ConfigDict(from_attributes=True)