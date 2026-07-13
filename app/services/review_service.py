from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.review import Review
from app.repositories.review_repository import ReviewRepository
from app.schemas.review import ReviewCreate, ReviewUpdate


class ReviewService:

    def __init__(self, db: Session):
        self.repository = ReviewRepository(db)

    def create_review(self, schema: ReviewCreate) -> Review:
        review = Review(
            title=schema.title,
            author=schema.author,
            decription=schema.description,
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
        book_id: int,
        schema: ReviewUpdate,
    ) -> Review:

        review = self.get_review(review_id)

        if schema.title is None and schema.author is None and schema.description is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided",
            )

        if schema.title is not None:
            review.title = schema.title

        if schema.author is not None:
            review.author = schema.author
        
        if schema.description is not None:
            review.description = schema.description

        return self.repository.update(review)

    def delete_review(self, review_id: int) -> None:
        review = self.get_review(review_id)

        self.repository.delete(review)