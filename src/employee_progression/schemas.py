from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProgressionBase(BaseModel):
    position_level: str
    salary: int
    start_date: datetime
    promotion_position_level: Optional[str]
    promotion_date: Optional[datetime]


class ProgressionRead(ProgressionBase):
    id: int

    class Config:
        orm_mode = True


class ProgressionCreate(ProgressionBase):
    pass

