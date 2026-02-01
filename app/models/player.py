from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PlayerBase(BaseModel):
    name: str

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(BaseModel):
    name: str

class PlayerRead(BaseModel):
    id: int
    name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

