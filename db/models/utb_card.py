from datetime import datetime
from typing import Optional, TYPE_CHECKING, List

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, Relationship

from db.models.base import BaseModel


from db.models.user import User
from db.models.photos import Photo


class Utb(BaseModel, table=True):
    in_number: Optional[str] = Field(nullable=False)
    car_going_date: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    car_going_place: Optional[str] = Field(nullable=False, default='')
    car_info: Optional[str] = Field(nullable=False)
    truck_info: Optional[str] = Field(nullable=False)
    license_plate: Optional[str] = Field(nullable=False, index=True)
    note: Optional[str] = Field(nullable=True)
    executor: Optional[str] = Field(nullable=False)
    owner: Optional[str] = Field(nullable=True)
    owner_phone: Optional[str] = Field(nullable=True)

    add_by_user_id: Optional[int] = Field(foreign_key="user.id", default=None, nullable=True)
    add_by_user: 'User' = Relationship(
        back_populates="utb_add_records",
        sa_relationship_kwargs=dict(foreign_keys="[Utb.add_by_user_id]"),
    )
    dkr: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    kr_by_user_id: Optional[int] = Field(foreign_key="user.id", default=None, nullable=True)
    kr_by_user: 'User' = Relationship(
        back_populates="utb_kr_records",
        sa_relationship_kwargs=dict(foreign_keys="[Utb.kr_by_user_id]"),
    )
    photos: List['Photo'] = Relationship(sa_relationship_kwargs={"cascade": "all, delete"}, back_populates="utb")
