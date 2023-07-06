from datetime import datetime

from sqlalchemy import String, func, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class EmployeeProgression(Base):
    __tablename__ = 'employee_progression'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    start_date: Mapped[datetime] = mapped_column(
        server_default=func.CURRENT_TIMESTAMP()
    )
    position_level: Mapped[str] = mapped_column(
        String(length=320), nullable=False
    )
    salary: Mapped[int] = mapped_column(nullable=False)
    promotion_position_level: Mapped[str] = mapped_column(
        String(length=320), nullable=True
    )
    promotion_date: Mapped[datetime] = mapped_column(
        nullable=True
    )
    employee: Mapped['User'] = relationship(
        back_populates='progression', uselist=False
    )


employee_progression = EmployeeProgression.__table__
