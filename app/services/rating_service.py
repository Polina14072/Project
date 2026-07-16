from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.rating import Rating
from app.repositories.rating_repository import RatingRepository
from app.schemas.rating import RatingCreate, RatingUpdate


class RatingService:

    def __init__(self, db: Session):
        self.repository = RatingRepository(db)

    def create_rating(self, schema: RatingCreate, user_id: int) -> Rating:
        existing = self.repository.get_by_user_and_film(user_id, schema.film_id)

        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already rated this film",
            )

        rating = Rating(
            score=schema.score,
            film_id=schema.film_id,
            user_id=user_id,
        )

        return self.repository.create(rating)

    def get_ratings(self) -> list[Rating]:
        return self.repository.get_all()

    def get_rating(self, rating_id: int) -> Rating:
        rating = self.repository.get_by_id(rating_id)

        if rating is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rating not found",
            )

        return rating

    def update_rating(self, rating_id: int, schema: RatingUpdate) -> Rating:
        rating = self.get_rating(rating_id)

        if schema.score is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Score must be provided",
            )

        rating.score = schema.score

        return self.repository.update(rating)

    def delete_rating(self, rating_id: int) -> None:
        rating = self.get_rating(rating_id)

        self.repository.delete(rating)