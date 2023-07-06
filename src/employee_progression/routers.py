from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_user, current_superuser
from src.auth.models import User
from src.database import get_async_session
from src.employee_progression.schemas import ProgressionRead
from src.employee_progression.service import (
    get_employees_progressions,
    get_employee_progression,
)

router = APIRouter(
    prefix='/employee-progressions',
    tags=['Employee Progressions']
)


@router.get('', response_model=List[ProgressionRead])
async def get_progressions(offset: int = 0,
                           limit: int = 10,
                           user: User = Depends(current_superuser),
                           session: AsyncSession = Depends(get_async_session)):
    result = await get_employees_progressions(session, offset, limit)

    return [ProgressionRead(**progression) for progression in result]


@router.get("/mine", response_model=ProgressionRead)
async def get_my_progression(
        user=Depends(current_user),
        session: AsyncSession = Depends(get_async_session)):
    result = await get_employee_progression(user, session)
    if not result:
        raise HTTPException(status_code=404, detail="Progression not found")
    return result
