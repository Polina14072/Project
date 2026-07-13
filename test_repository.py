from app.database import Base, SessionLocal, engine
from app.models.film import Film
from app.repositories.film_repository import FilmRepository

Base.metadata.create_all(bind=engine)

db = SessionLocal()

repository = FilmRepository(db)

film = Film(
    title="Высоконагруженные приложения",
    director="Мартин Клеппман",
)

repository.create(film)

film = repository.get_all()

for film in film:
    print(film.id, film.title, film.director)

db.close()