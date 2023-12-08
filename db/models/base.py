from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr


class BaseModel(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __table_args__(cls) -> dict:
        return {'extend_existing': True}

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(default=None, primary_key=True)
    dvv: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
