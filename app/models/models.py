from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass  # noqa: WPS604, WPS420


class Content(Base):
    __tablename__ = "saved_content"

    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003, VNE003
    file_unique_id: Mapped[str] = mapped_column(String(512), unique=True)
