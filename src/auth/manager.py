from typing import Optional

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
    exceptions,
    models,
    schemas
)
from fastapi_users.db import BaseUserDatabase
from fastapi_users.password import PasswordHelperProtocol, PasswordHelper
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError

from src.auth.models import User
from src.auth.utils import get_user_db
from src.config import SECRET_AUTH


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_AUTH
    verification_token_secret = SECRET_AUTH

    async def authenticate(
        self, credentials: OAuth2PasswordRequestForm
    ) -> Optional[models.UP]:
        try:
            user = await self.get_by_username(credentials.username)
        except exceptions.UserNotExists:
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None
        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        return user

    async def get_by_username(self, username: str) -> models.UP:
        query = select(self.user_db.user_table).where(
            func.lower(self.user_db.user_table.username) == func.lower(username)
        )

        results = await self.user_db.session.execute(query)

        user = results.unique().scalar_one_or_none()

        if user is None:
            raise exceptions.UserNotExists()

        return user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
