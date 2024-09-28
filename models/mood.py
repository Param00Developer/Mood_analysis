from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MoodScore(BaseModel):
    _id: str
    field: str
    user: str
    value: int
    createdAt: datetime = datetime.isoformat()
    updatedAt: datetime = datetime.isoformat()

    class Config:
        allow_population_by_field_name = True

    def __init__(self, **data):
        super().__init__(**data)
        self.updatedAt = datetime.isoformat()