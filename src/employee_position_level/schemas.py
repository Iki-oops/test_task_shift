from pydantic import BaseModel, Field


class Employee(BaseModel):
    id: int
    username: str
    email: str
    first_name: str = Field(alias='firstName')
    last_name: str = Field(alias='lastName')
    salary: int = Field(ge=0)

    class Config:
        populate_by_name = True


class PositionLevelBase(BaseModel):
    position_level: str
    min_salary: int = Field(ge=0, alias='minSalary')
    max_salary: int = Field(ge=0, alias='maxSalary')
    employees: list[Employee] = []

    class Config:
        populate_by_name = True


class PositionLevelRead(PositionLevelBase):
    id: int
