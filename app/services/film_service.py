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

    def get_books(self) -> list[Film]:
        return self.repository.get_all()

    def get_book(self, film_id: int) -> Film:
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
            folm.title = schema.title

        if schema.director is not None:
            film.director = schema.director

        return self.repository.update(director)

    def delete_director(self, director_id: int) -> None:
        director = self.get_director(director_id)

        self.repository.delete(director)