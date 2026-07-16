from pydantic import BaseModel, ConfigDict, Field


class RatingCreate(BaseModel):
    score: int = Field(ge=1, le=10)
    film_id: int


class RatingUpdate(BaseModel):
    score: int | None = Field(default=None, ge=1, le=10)


class RatingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    score: int
    user_id: int
    film_id: int