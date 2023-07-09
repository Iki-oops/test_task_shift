from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_user, current_superuser
from src.auth.models import User
from src.database import get_async_session
from src.employee_progression.exceptions import SalaryOutOfRange
from src.employee_progression.schemas import ProgressionRead, ProgressionCreate
from src.employee_progression.service import (
    get_employees_progressions,
    get_employee_progression, add_new_employee_progression,
)

router = APIRouter(
    prefix='/employee-progressions',
    tags=['Employee Progressions']
)


@router.get('')
async def get_progressions(offset: int = 0,
                           limit: int = 10,
                           user: User = Depends(current_superuser),
                           session: AsyncSession = Depends(get_async_session)):
    result = await get_employees_progressions(session, offset, limit)
    result = [ProgressionRead(**row) for row in result]

    return {
        'status': 'success',
        'data': result,
        'detail': None
    }


@router.post('',
             status_code=status.HTTP_201_CREATED)
async def add_progression(
        new_progression: ProgressionCreate,
        user=Depends(current_superuser),
        session: AsyncSession = Depends(get_async_session)):
    try:
        result = await add_new_employee_progression(
            dict(new_progression), session
        )
        return {
            'status': 'success',
            'data': ProgressionCreate(**result),
            'detail': None
        }
    except SalaryOutOfRange:
        return JSONResponse(
            content={
                'status': 'error',
                'data': None,
                'detail': 'salary out of range min_salary or max_salary'
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )
    except Exception as error:
        return JSONResponse(
            content={
                'status': 'error',
                'data': None,
                'detail': error
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.get("/mine")
async def get_my_progression(
        user=Depends(current_user),
        session: AsyncSession = Depends(get_async_session)):
    result = await get_employee_progression(user, session)
    return {
        'status': 'success',
        'data': ProgressionRead(**result),
        'detail': None
    }
