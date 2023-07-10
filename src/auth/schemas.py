from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr, Field


class UserRead(schemas.BaseUser[int]):
    id: int
    username: str
    email: EmailStr
    first_name: Optional[str] = Field(default=None, alias='firstName')
    last_name: Optional[str] = Field(default=None, alias='lastName')
    is_active: bool = Field(default=True, alias='isActive')
    is_superuser: bool = Field(default=False, alias='isSuperUser')
    is_verified: bool = Field(default=False, alias='isVerified')

    class Config:
        # orm_mode = True
        populate_by_name = True
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    first_name: Optional[str] = Field(default=None, alias='firstName')
    last_name: Optional[str] = Field(default=None, alias='lastName')
    password: str
    is_active: Optional[bool] = Field(default=True, alias='isActive')
    is_superuser: Optional[bool] = Field(default=False, alias='isSuperUser')
    is_verified: Optional[bool] = Field(default=False, alias='isVerified')

    class Config:
        populate_by_name = True
