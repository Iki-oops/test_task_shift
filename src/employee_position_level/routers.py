from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_superuser
from src.database import get_async_session
from src.employee_position_level.schemas import PositionLevelRead
from src.employee_position_level.service import (
    get_employee_position_levels,
    get_employee_position_level
)

router = APIRouter(
    prefix='/employee-position-levels',
    tags=['Employee Position Levels']
)


@router.get('')
async def get_position_levels(
        offset: int = 0,
        limit: int = 10,
        user=Depends(current_superuser),
        session: AsyncSession = Depends(get_async_session)):
    result = await get_employee_position_levels(session, offset, limit)

    return {
        'status': 'success',
        'data': result,
        'detail': None,
    }


@router.get('/{position_level}')
async def get_position_level(
        position_level: str,
        user=Depends(current_superuser),
        session: AsyncSession = Depends(get_async_session)):
    try:
        result = await get_employee_position_level(session, position_level)

        return {
            'status': 'success',
            'data': PositionLevelRead(**result),
            'detail': None,
        }
    except IndexError:
        return JSONResponse(
            content={
                'status': 'success',
                'data': None,
                'detail': 'not found position level',
            },
            status_code=status.HTTP_404_NOT_FOUND
        )
