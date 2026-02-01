from pydantic import BaseModel, ConfigDict


class TeamBase(BaseModel):
    name: str
    short_name: str | None = None

class TeamRead(TeamBase):
    id: int
    external_id: int | None = None

    model_config = ConfigDict(from_attributes=True)
