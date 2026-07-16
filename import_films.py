import json

from app.database import SessionLocal
import app.models  # noqa: F401 — регистрирует все модели в SQLAlchemy
from app.schemas.film import FilmCreate
from app.services.film_service import FilmService


def main():
    with open("data/films.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    db = SessionLocal()
    try:
        service = FilmService(db)
        created_count = 0
        skipped_count = 0

        for key, value in data.items():
            existing = service.get_by_title(value["title"])
            if existing is not None:
                print(f"Пропущено (уже существует): {value['title']}")
                skipped_count += 1
                continue

            schema = FilmCreate(
                title=value["title"],
                director=value["director"],
            )
            service.create_film(schema)
            print(f"Импортирован фильм: {schema.title}")
            created_count += 1

        print(f"Готово. Импортировано: {created_count}, пропущено: {skipped_count}")
    finally:
        db.close()


if __name__ == "__main__":
    main()