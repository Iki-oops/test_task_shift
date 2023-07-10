from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProgressionBase(BaseModel):
    current_position_date: datetime = Field(alias='currentPositionDate')
    salary: int = Field(ge=0)
    promotion_position_date: Optional[datetime] = Field(
        default=None,
        alias='promotionPositionDate'
    )

    class Config:
        populate_by_name = True


class ProgressionRead(ProgressionBase):
    id: int
    current_position_level: str = Field(alias='currentPositionLevel')
    promotion_position_level: Optional[str] = Field(
        default=None,
        alias='promotionPositionLevel'
    )

    class Config:
        from_attributes = True


class ProgressionCreate(ProgressionBase):
    current_position_level_id: int = Field(alias='currentPositionLevelId')
    promotion_position_level_id: Optional[int] = Field(
        default=None,
        alias='promotionPositionLevelId'
    )
