from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import (
    Integer,
    String,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database import Base
from src.employee_progression.models import employee_progression


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "employee"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    username: Mapped[str] = mapped_column(
        String(length=320), unique=True, nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    first_name: Mapped[str] = mapped_column(
        String(length=320), nullable=False
    )
    last_name: Mapped[str] = mapped_column(
        String(length=320), nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    progression_id: Mapped[int] = mapped_column(
        ForeignKey(employee_progression.c.id), nullable=True
    )
    progression: Mapped['EmployeeProgression'] = relationship(
        back_populates='employee',
    )


employee = User.__table__
