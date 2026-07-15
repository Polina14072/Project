from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.review import Review
from app.repositories.review_repository import ReviewRepository
from app.schemas.review import ReviewCreate, ReviewUpdate


class ReviewService:

    def __init__(self, db: Session):
        self.repository = ReviewRepository(db)

    def create_review(self, schema: ReviewCreate, user_id: int) -> Review:
        review = Review(
            text=schema.text,
            film_id=schema.film_id,
            user_id=user_id,
        )

        return self.repository.create(review)

    def get_reviews(self) -> list[Review]:
        return self.repository.get_all()

    def get_review(self, review_id: int) -> Review:
        review = self.repository.get_by_id(review_id)

        if review is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found",
            )

        return review

    def update_review(
        self,
        review_id: int,
        schema: ReviewUpdate,
    ) -> Review:
        review = self.get_review(review_id)

        if schema.text is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text must be provided",
            )

        review.text = schema.text

        return self.repository.update(review)

    def delete_review(self, review_id: int) -> None:
        review = self.get_review(review_id)

        self.repository.delete(review)