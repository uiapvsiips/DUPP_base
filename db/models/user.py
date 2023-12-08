import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import BaseModel

if TYPE_CHECKING:
    from db.models.utb_card import Utb


class User(BaseModel):
    id: Mapped[int] = mapped_column(default=None, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    middle_name: Mapped[str] = mapped_column(nullable=True)
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)
    tgid: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=True)
    tg_confirm_guid: Mapped[str] = mapped_column(unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    utb_add_records: Mapped[List['Utb']] = relationship(back_populates="add_by_user",
                                                        primaryjoin='Utb.add_by_user_id == User.id',
                                                        cascade="all, delete",)
    utb_kr_records: Mapped[List['Utb']] = relationship(back_populates="kr_by_user",
                                                       primaryjoin='Utb.kr_by_user_id == User.id',
                                                       cascade="all, delete")

    def dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "middle_name": self.middle_name,
            "is_admin": self.is_admin,
            "tgid": self.tgid,
            "tg_confirm_guid": self.tg_confirm_guid,
        }


if __name__ == '__main__':
    user = User()
    d = 1
