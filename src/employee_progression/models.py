from datetime import datetime

from sqlalchemy import func, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.employee_position_level.models import (
    employee_position_level,
    EmployeePositionLevel,
)


class EmployeeProgression(Base):
    __tablename__ = 'employee_progression'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    current_position_level_id: Mapped[int] = mapped_column(
        ForeignKey(employee_position_level.c.id),
        nullable=False,
        default=EmployeePositionLevel.POSITION_LEVEL_INITIAL
    )
    current_position_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.CURRENT_TIMESTAMP()
    )
    salary: Mapped[int] = mapped_column(nullable=False)
    promotion_position_level_id: Mapped[int] = mapped_column(
        ForeignKey(employee_position_level.c.id), nullable=True
    )
    promotion_position_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    employee: Mapped['User'] = relationship(
        back_populates='progression',
        uselist=False
    )
    current_position_level: Mapped['EmployeePositionLevel'] = relationship(
        foreign_keys=[current_position_level_id],
        back_populates='current_progression'
    )
    promotion_position_level: Mapped['EmployeePositionLevel'] = relationship(
        foreign_keys=[promotion_position_level_id],
        back_populates='promotion_progression'
    )


employee_progression = EmployeeProgression.__table__
