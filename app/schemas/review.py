from pydantic import BaseModel, ConfigDict, Field


class ReviewCreate(BaseModel):
    text: str = Field(min_length=1, max_length=200)
    film_id: str = Field(min_length=1, max_length=200)
    


class ReviewUpdate(BaseModel):
    text: str | None = Field(default=None, min_length=1, max_length=200)
    film_id: str | None = Field(default=None, min_length=1, max_length=200)
    


class ReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    film_id: int