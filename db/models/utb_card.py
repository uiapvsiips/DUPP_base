from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

from db.models.base import BaseModel

if TYPE_CHECKING:
    from db.models.photos import Photo
    from db.models.user import User


class Utb(BaseModel):
    id: Mapped[int] = mapped_column(default=None, primary_key=True)
    in_number: Mapped[str] = mapped_column(nullable=False)
    car_going_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    car_going_place: Mapped[str] = mapped_column(nullable=False, default='')
    car_info: Mapped[str] = mapped_column(nullable=False, index=True)
    truck_info: Mapped[str] = mapped_column(nullable=False)
    license_plate: Mapped[str] = mapped_column(nullable=False, index=True)
    note: Mapped[str] = mapped_column(nullable=True, index=True)
    executor: Mapped[str] = mapped_column(nullable=False)
    owner: Mapped[str] = mapped_column(nullable=True)
    owner_phone: Mapped[str] = mapped_column(nullable=True, index=True)

    add_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), default=None, nullable=True)
    add_by_user: Mapped['User'] = relationship(back_populates="utb_add_records", foreign_keys=add_by_user_id)

    dkr: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    kr_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), default=None, nullable=True)
    kr_by_user: Mapped['User'] = relationship(back_populates="utb_kr_records", foreign_keys=kr_by_user_id)

    photos: Mapped[List['Photo']] = relationship(cascade="all, delete", back_populates="utb",
                                                 primaryjoin='Photo.utb_id==Utb.id')
