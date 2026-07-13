from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.rating import Rating
from app.repositories.rating_repository import RatingRepository
from app.schemas.rating import RatingCreate, RatingUpdate


class RatingService:

    def __init__(self, db: Session):
        self.repository = RatingRepository(db)

    def create_rating(self, schema: RatingCreate) -> Rating:
        rating = Rating(
            title=schema.title,
            author=schema.author,
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

    def update_rating(
        self,
        rating_id: int,
        schema: RatingUpdate,
    ) -> Rating:

        rating = self.get_rating(rating_id)

        if schema.title is None and schema.author is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided",
            )

        if schema.title is not None:
            rating.title = schema.title

        if schema.author is not None:
            rating.author = schema.author

        return self.repository.update(rating)

    def delete_rating(self, rating_id: int) -> None:
        rating = self.get_rating(rating_id)

        self.repository.delete(rating)