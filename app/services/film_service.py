from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.film import Film
from app.repositories.film_repository import FilmRepository
from app.schemas.film import FilmCreate, FilmUpdate


class FilmService:

    def __init__(self, db: Session):
        self.repository = FilmRepository(db)

    def create_film(self, schema: FilmCreate) -> Film:
        film = Film(
            title=schema.title,
            director=schema.director,
        )

        return self.repository.create(film)

    def get_films(self) -> list[Film]:
        return self.repository.get_all()
        
    def get_by_title(self, title: str) -> Film | None:
        return self.repository.get_by_title(title)

    def get_film(self, film_id: int) -> Film:
        film = self.repository.get_by_id(film_id)

        if film is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Film not found",
            )

        return film

    def update_film(
        self,
        film_id: int,
        schema: FilmUpdate,
    ) -> Film:

        film = self.get_film(film_id)

        if schema.title is None and schema.director is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one field must be provided",
            )

        if schema.title is not None:
            film.title = schema.title

        if schema.director is not None:
            film.director = schema.director

        return self.repository.update(film)

    def delete_film(self, film_id: int) -> None:
        film = self.get_film(film_id)

        self.repository.delete(film)