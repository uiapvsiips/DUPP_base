from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, func, BigInteger, Integer, ForeignKey
from sqlmodel import SQLModel, Field, Relationship


class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    dvv: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )


class User(BaseModel, table=True):
    username: Optional[str] = Field(nullable=False)
    password: Optional[str] = Field(nullable=False)
    first_name: Optional[str] = Field(nullable=False)
    last_name: Optional[str] = Field(nullable=False)
    middle_name: Optional[str] = Field(nullable=True)
    is_admin: Optional[bool] = Field(nullable=False, default=False)
    tgid: Optional[int] = Field(sa_column=Column(BigInteger()))
    utb_add_records: list["Utb"] = Relationship(
        back_populates="add_by_user",
        sa_relationship_kwargs={
            "primaryjoin": "Utb.add_by_user_id==User.id",
            "lazy": "joined",
        }, )
    utb_kr_records: list["Utb"] = Relationship(
        back_populates="kr_by_user",
        sa_relationship_kwargs={
            "primaryjoin": "Utb.kr_by_user_id==User.id",
            "lazy": "joined",
        }, )


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
    add_by_user: "User" = Relationship(
        back_populates="utb_add_records",
        sa_relationship_kwargs=dict(foreign_keys="[Utb.add_by_user_id]"),
    )
    dkr: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    kr_by_user_id: Optional[int] = Field(foreign_key="user.id", default=None, nullable=True)
    kr_by_user: "User" = Relationship(
        back_populates="utb_kr_records",
        sa_relationship_kwargs=dict(foreign_keys="[Utb.kr_by_user_id]"),
    )
    photos: list["Photo"] = Relationship(sa_relationship_kwargs={"cascade": "all, delete"}, back_populates="utb")


class Photo(BaseModel, table=True):
    utb_id: Optional[int] = Field(sa_column=Column(Integer, ForeignKey("utb.id", ondelete="CASCADE"), index=True) )
    utb: "Utb" = Relationship(back_populates="photos")
    photo: Optional[str] = Field(nullable=True)


if __name__ == '__main__':
    utb = Utb()
    d = 1
