from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, TEXT
from sqlalchemy.orm import Mapped, relationship, mapped_column

from db.models.base import BaseModel

if TYPE_CHECKING:
    from db.models.utb_card import Utb


class Photo(BaseModel):
    utb_id: Mapped[int] = mapped_column(ForeignKey("utbs.id"), index=True)
    utb: Mapped['Utb'] = relationship(back_populates="photos", cascade="all, delete", foreign_keys=utb_id)
    photo: Mapped[bytes] = mapped_column(nullable=True)
