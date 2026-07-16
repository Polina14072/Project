from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.rating import RatingCreate, RatingResponse, RatingUpdate
from app.services.rating_service import RatingService

router = APIRouter(
    prefix="/ratings",
    tags=["ratings"],
)


def get_rating_service(
    db: Session = Depends(get_db),
) -> RatingService:
    return RatingService(db)


@router.post(
    "/",
    response_model=RatingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_rating(
    schema: RatingCreate,
    current_user: User = Depends(get_current_user),
    service: RatingService = Depends(get_rating_service),
):
    return service.create_rating(schema, current_user.id)


@router.get(
    "/",
    response_model=list[RatingResponse],
)
def get_ratings(
    service: RatingService = Depends(get_rating_service),
):
    return service.get_ratings()


@router.get(
    "/{rating_id}",
    response_model=RatingResponse,
)
def get_rating(
    rating_id: int,
    service: RatingService = Depends(get_rating_service),
):
    return service.get_rating(rating_id)


@router.patch(
    "/{rating_id}",
    response_model=RatingResponse,
)
def update_rating(
    rating_id: int,
    schema: RatingUpdate,
    service: RatingService = Depends(get_rating_service),
):
    return service.update_rating(rating_id, schema)


@router.delete(
    "/{rating_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_rating(
    rating_id: int,
    service: RatingService = Depends(get_rating_service),
) -> None:
    service.delete_rating(rating_id)