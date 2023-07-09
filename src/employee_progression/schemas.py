from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProgressionBase(BaseModel):
    current_position_level_id: int = Field(alias='currentPositionLevelId')
    current_position_date: datetime = Field(alias='currentPositionDate')
    salary: int = Field(ge=0)
    promotion_position_level_id: Optional[int] = Field(
        alias='promotionPositionLevelId'
    )
    promotion_position_date: Optional[datetime] = Field(
        alias='promotionPositionDate'
    )

    class Config:
        allow_population_by_field_name = True


class ProgressionRead(ProgressionBase):
    id: int

    class Config:
        orm_mode = True


class ProgressionCreate(ProgressionBase):
    pass

