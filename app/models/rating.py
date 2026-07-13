from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Rating(Base):
    __tablename__ = "ratings"

    id: Mapped[int] = mapped_column(primary_key=True)

    score: Mapped[int] = mapped_column()

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )
    
    film_id: Mapped[int] = mapped_column(
        ForeignKey("films.id")
    )

    user: Mapped["User"] = relationship(
        back_populates="ratings"
    )

    film: Mapped["Film"] = relationship(
        back_populates="ratings"
    )