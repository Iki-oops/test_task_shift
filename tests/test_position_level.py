import datetime

from sqlalchemy import insert, select

from conftest import client, async_session_maker
from src.employee_position_level.models import employee_position_level
from src.employee_position_level.service import get_employee_position_levels
from src.employee_progression.models import employee_progression


async def test_add_position_level():
    async with async_session_maker() as session:
        statement = insert(employee_position_level).values(
            id=1,
            position_level='newbie',
            min_salary=1000,
            max_salary=3000,
        )
        await session.execute(statement)
        await session.commit()


async def test_add_progression():
    async with async_session_maker() as session:
        statement = insert(employee_progression).values(
            id=2,
            current_position_level_id=1,
            current_position_date=datetime.datetime.now(datetime.timezone.utc),
            salary=2000,
            promotion_position_level_id=1,
            promotion_position_date=datetime.datetime.now(datetime.timezone.utc),
        )
        await session.execute(statement)
        await session.commit()


async def test_get_position_levels(superuser_client):
    async with async_session_maker() as session:
        await get_employee_position_levels(session, 0, 10)
    response = await superuser_client.get('/employee-position-levels')
    assert response.status_code == 200


# async def test_get_position_level(current_user_client, setup_add_progression):
#     response = await current_user_client.get('/employee-progressions/mine')
#     assert response.status_code == 200
