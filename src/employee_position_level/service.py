from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from src.auth.models import employee
from src.employee_position_level.models import employee_position_level
from src.employee_progression.models import employee_progression


def get_default_query_employee_position_levels(offset: int = 0,
                                               limit: int = 10,
                                               **kwargs):
    epl = aliased(employee_position_level)
    ep = aliased(employee_progression)

    query = (
        select(
            epl.c.id.label('position_level_id'),
            epl.c.position_level,
            epl.c.min_salary,
            epl.c.max_salary,
        )
        .order_by('position_level')
        .limit(limit)
        .offset(offset)
    )

    if kwargs.get('position_level'):
        query = query.filter(
            epl.c.position_level == kwargs.get('position_level')
        )

    query = query.subquery()

    query = (
        select(
            query,
            ep.c.salary,
            ep.c.id.label('progression_id'),
        )
        .join(
            ep, ep.c.current_position_level_id == query.c.position_level_id
        ).subquery()
    )

    query = (
        select(
            employee.c.id.label('employee_id'),
            employee.c.username,
            employee.c.email,
            employee.c.first_name,
            employee.c.last_name,
            query
        )
        .join(query, query.c.progression_id == employee.c.progression_id)
    )

    return query


def format_employee_position_levels(data):
    result = []
    for row in data:
        emp = {
            'id': row.employee_id,
            'username': row.username,
            'email': row.email,
            'first_name': row.first_name,
            'last_name': row.last_name,
            'salary': row.salary,
        }

        position_level_row = list(
            filter(
                lambda x: x.get('position_level') == row.position_level, result
            )
        )

        if position_level_row:
            position_level_row[0]['employees'].append(emp)
        else:
            result.append(
                {
                    'id': row.position_level_id,
                    'position_level': row.position_level,
                    'min_salary': row.min_salary,
                    'max_salary': row.max_salary,
                    'employees': [emp],
                }
            )

    return result


async def get_employee_position_levels(session: AsyncSession, offset, limit):
    query = get_default_query_employee_position_levels(offset, limit)
    data = (await session.execute(query)).all()

    return format_employee_position_levels(data)


async def get_employee_position_level(session: AsyncSession,
                                      position_level: str):
    query = get_default_query_employee_position_levels(
        position_level=position_level
    )

    data = (await session.execute(query)).all()

    return format_employee_position_levels(data)[0]
