from sqlalchemy import String, func, TIMESTAMP
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Content(Base):
    __tablename__ = "saved_content"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_unique_id: Mapped[str] = mapped_column(String(512), unique=True)
