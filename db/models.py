from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field


class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    dvv: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )


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


