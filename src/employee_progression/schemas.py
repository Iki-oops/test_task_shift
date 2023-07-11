from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class ProgressionBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    current_position_date: datetime = Field(alias='currentPositionDate')
    salary: int = Field(ge=0)
    promotion_position_date: datetime | None = Field(
        default=None,
        alias='promotionPositionDate'
    )


class ProgressionRead(ProgressionBase):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int
    current_position_level: str = Field(alias='currentPositionLevel')
    promotion_position_level: str | None = Field(
        default=None,
        alias='promotionPositionLevel'
    )


class ProgressionCreate(ProgressionBase):
    current_position_level_id: int = Field(alias='currentPositionLevelId')
    promotion_position_level_id: int | None = Field(
        default=None,
        alias='promotionPositionLevelId'
    )
