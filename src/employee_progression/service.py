from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.employee_progression.models import employee_progression


async def get_employees_progressions(session: AsyncSession,
                                     offset: int = 0,
                                     limit: int = 10):
    query = select(employee_progression)\
        .order_by(employee_progression.c.salary.desc())\
        .offset(offset).limit(limit)
    data = (await session.execute(query)).all()

    result = [row._asdict() for row in data]

    return result


async def get_employee_progression(user: int, session: AsyncSession):
    query = select(employee_progression)\
        .where(employee_progression.c.id == user.progression_id)
    data = (await session.execute(query)).first()

    if data:
        return data._asdict()

    return
