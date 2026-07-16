from sqlalchemy.orm import Session

from app.models.rating import Rating


class RatingRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, rating: Rating) -> Rating:
        return self._upsert(rating)

    def update(self, rating: Rating) -> Rating:
        return self._upsert(rating)

    def _upsert(self, rating: Rating) -> Rating:
        self.db.add(rating)
        self.db.commit()
        self.db.refresh(rating)

        return rating

    def get_all(self) -> list[Rating]:
        return self.db.query(Rating).all()

    def get_by_id(self, rating_id: int) -> Rating | None:
        return (
            self.db.query(Rating)
            .filter(Rating.id == rating_id)
            .first()
        )

    def get_by_user_and_film(self, user_id: int, film_id: int) -> Rating | None:
        return (
            self.db.query(Rating)
            .filter(Rating.user_id == user_id, Rating.film_id == film_id)
            .first()
        )

    def delete(self, rating: Rating) -> None:
        self.db.delete(rating)
        self.db.commit()