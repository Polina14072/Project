from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Film(Base):
    __tablename__ = "films"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(String, nullable=False)

    director: Mapped[str] = mapped_column(String, nullable=False)

    reviews: Mapped[list["Review"]] = relationship(
        back_populates="film",
    )

    ratings: Mapped[list["Rating"]] = relationship(
        back_populates="film",
    )