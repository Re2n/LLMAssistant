from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from models.Base import Base
from models.mixins.int_id_pk import IntIdPkMixin


class Message(Base, IntIdPkMixin):
    __tablename__ = "messages"
    text: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column(default="new")  # new/pending/approved/rejected
    chat_id: Mapped[int] = mapped_column(BigInteger)
    response_text: Mapped[str] = mapped_column(nullable=True)  # Ответ для отправки в TG