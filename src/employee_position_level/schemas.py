from pydantic import BaseModel, Field, ConfigDict


class Employee(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    username: str
    email: str
    first_name: str = Field(alias='firstName')
    last_name: str = Field(alias='lastName')
    salary: int = Field(ge=0)


class PositionLevelBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    position_level: str
    min_salary: int = Field(ge=0, alias='minSalary')
    max_salary: int = Field(ge=0, alias='maxSalary')
    employees: list[Employee] = []


class PositionLevelRead(PositionLevelBase):
    id: int
