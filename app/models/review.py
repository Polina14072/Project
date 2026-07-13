from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base



class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    text: Mapped[str] = mapped_column(String)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    film_id: Mapped[int] = mapped_column(
        ForeignKey("films.id")
    )

    user: Mapped["User"] = relationship(
        back_populates="reviews",
    )

    film: Mapped["Film"] = relationship(
        back_populates="reviews"
    )
    

