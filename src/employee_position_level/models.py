from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database import Base


class EmployeePositionLevel(Base):
    __tablename__ = 'employee_position_level'
    POSITION_LEVEL_INITIAL = 1

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    position_level: Mapped[str] = mapped_column(
        String(320), nullable=False, unique=True
    )
    min_salary: Mapped[int] = mapped_column(nullable=False)
    max_salary: Mapped[int] = mapped_column(nullable=False)
    current_progression: Mapped['EmployeeProgression'] = relationship(
        foreign_keys='EmployeeProgression.current_position_level_id',
        back_populates='current_position_level',
        uselist=False,
    )
    promotion_progression: Mapped['EmployeeProgression'] = relationship(
        foreign_keys='EmployeeProgression.promotion_position_level_id',
        back_populates='promotion_position_level',
        uselist=False,
    )


employee_position_level = EmployeePositionLevel.__table__
