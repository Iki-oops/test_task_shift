from fastapi_users import schemas
from pydantic import EmailStr, Field, ConfigDict


class UserRead(schemas.BaseUser[int]):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int
    username: str
    email: EmailStr
    first_name: str | None = Field(default=None, alias='firstName')
    last_name: str | None = Field(default=None, alias='lastName')
    is_active: bool = Field(default=True, alias='isActive')
    is_superuser: bool = Field(default=False, alias='isSuperUser')
    is_verified: bool = Field(default=False, alias='isVerified')


class UserCreate(schemas.BaseUserCreate):
    model_config = ConfigDict(populate_by_name=True)

    username: str
    email: EmailStr
    first_name: str | None = Field(default=None, alias='firstName')
    last_name: str | None = Field(default=None, alias='lastName')
    password: str
    is_active: bool = Field(default=True, alias='isActive')
    is_superuser: bool = Field(default=False, alias='isSuperUser')
    is_verified: bool = Field(default=False, alias='isVerified')
