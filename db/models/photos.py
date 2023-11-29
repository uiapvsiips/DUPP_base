from typing import Optional, TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey
from sqlmodel import Field, Relationship

from db.models.base import BaseModel

if TYPE_CHECKING:
    from db.models.utb_card import Utb


class Photo(BaseModel, table=True):
    utb_id: Optional[int] = Field(sa_column=Column(Integer, ForeignKey("utb.id", ondelete="CASCADE"), index=True))
    utb: 'Utb' = Relationship(back_populates="photos")
    photo: Optional[str] = Field(nullable=True)
