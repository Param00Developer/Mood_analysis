from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class User(BaseModel):
    _id: str
    name: str
    timezone: str
    version: int
    app: str
    country: str
    createdAt: str = datetime.utcnow().isoformat()
    updatedAt: str = datetime.utcnow().isoformat()

    class Config:
        allow_population_by_field_name = True

    def __init__(self, **data):
        super().__init__(**data)
        self.updatedAt = datetime.utcnow().isoformat()