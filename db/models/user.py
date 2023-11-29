from typing import Optional, TYPE_CHECKING

from sqlalchemy import Column, BigInteger
from sqlmodel import Field, Relationship

from db.models.base import BaseModel

if TYPE_CHECKING:
    from db.models.utb_card import Utb
else:
    Utb = 'Utb'



class User(BaseModel, table=True):
    username: Optional[str] = Field(nullable=False)
    password: Optional[str] = Field(nullable=False)
    first_name: Optional[str] = Field(nullable=False)
    last_name: Optional[str] = Field(nullable=False)
    middle_name: Optional[str] = Field(nullable=True)
    is_admin: Optional[bool] = Field(nullable=False, default=False)
    tgid: Optional[int] = Field(sa_column=Column(BigInteger()))
    utb_add_records: list[Utb] = Relationship(
        back_populates="add_by_user",
        sa_relationship_kwargs={
            "primaryjoin": "Utb.add_by_user_id==User.id",
            "lazy": "joined",
        }, )
    utb_kr_records: list[Utb] = Relationship(
        back_populates="kr_by_user",
        sa_relationship_kwargs={
            "primaryjoin": "Utb.kr_by_user_id==User.id",
            "lazy": "joined",
        }, )