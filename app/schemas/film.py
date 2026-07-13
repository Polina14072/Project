from pydantic import BaseModel, ConfigDict, Field


class FilmCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    director: str = Field(min_length=1, max_length=200)


class FilmUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    director: str | None = Field(default=None, min_length=1, max_length=200)


class FilmResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    director: str