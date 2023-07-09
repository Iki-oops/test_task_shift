from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from src.auth.models import User
from src.employee_position_level.models import employee_position_level
from src.employee_progression.exceptions import SalaryOutOfRange
from src.employee_progression.models import employee_progression


def get_default_query_employees_progressions():
    """
    Базовый запрос для получения прогрессии сотрудников.
    """

    ep = aliased(employee_progression)
    current_pl = aliased(employee_position_level)
    promotion_pl = aliased(employee_position_level)

    query = (
        select(
            ep.c.id,
            ep.c.salary,
            current_pl.c.position_level.label('current_position_level'),
            ep.c.current_position_date,
            promotion_pl.c.position_level.label('promotion_position_level'),
            ep.c.promotion_position_date,
        )
        .join(
            current_pl,
            current_pl.c.id == ep.c.current_position_level_id,
        )
        .join(
            promotion_pl,
            promotion_pl.c.id == ep.c.promotion_position_level_id,
        )
    )
    return query


async def get_employees_progressions(session: AsyncSession,
                                     offset: int = 0,
                                     limit: int = 10):
    query = (
        get_default_query_employees_progressions()
        .offset(offset)
        .limit(limit)
    )
    data = (await session.execute(query)).all()

    return [row._asdict() for row in data]


async def get_employee_progression(user: User, session: AsyncSession):
    query = (
        get_default_query_employees_progressions()
        .where(employee_progression.c.id == user.progression_id)
    )
    data = (await session.execute(query)).first()

    return data._asdict() if data else {}


async def add_new_employee_progression(new_progression: dict,
                                       session: AsyncSession):
    epl = aliased(employee_position_level)
    salary = new_progression.get('salary')

    query = (
        select(epl)
        .where(epl.c.id == new_progression.get('current_position_level_id'))
    )

    position_level = (await session.execute(query)).first()
    min_salary, max_salary = (position_level.min_salary,
                              position_level.max_salary)

    if salary < min_salary or salary > max_salary:
        raise SalaryOutOfRange

    statement = (
        insert(employee_progression)
        .values(**new_progression)
        .returning(employee_progression)
    )
    result = await session.execute(statement)
    await session.commit()

    return result.first()._asdict()
