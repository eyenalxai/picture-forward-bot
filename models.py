from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Content(Base):
    __tablename__ = "saved_content"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_unique_id: Mapped[str] = mapped_column(String(512), unique=True)
