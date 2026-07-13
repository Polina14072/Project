from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.review import ReviewCreate, ReviewResponse, ReviewUpdate
from app.services.review_service import ReviewService

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
)


def get_review_service(
    db: Session = Depends(get_db),
) -> ReviewService:
    return ReviewService(db)


@router.post(
    "/",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_book(
    schema: ReviewCreate,
    service: ReviewService = Depends(get_review_service),
):
    return service.create_review(schema)


@router.get(
    "/",
    response_model=list[ReviewResponse],
)
def get_reviews(
    service: ReviewService = Depends(get_review_service),
):
    return service.get_reviews()


@router.get(
    "/{book_id}",
    response_model=ReviewResponse,
)
def get_review(
    book_id: int,
    service: ReviewService = Depends(get_review_service),
):
    return service.get_review(review_id)


@router.patch(
    "/{book_id}",
    response_model=ReviewResponse,
)
def update_review(
    review_id: int,
    schema: ReviewUpdate,
    service: ReviewService = Depends(get_review_service),
):
    return service.update_review(review_id, schema)


@router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_review(
    review_id: int,
    service: ReviewService = Depends(get_review_service),
) -> None:
    service.delete_review(review_id)