import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup


PAGE_URL = (
    "https://books.toscrape.com/"
    "catalogue/category/books_1/page-2.html"
)

OUTPUT_FILE = Path("data/films.json")

# У демо-сайта нет данных о режиссёре — используем заглушку.
# Когда появится реальный источник с этим полем, замените
# на реальное значение из HTML.
UNKNOWN_DIRECTOR = "Неизвестно"


def get_page_html(url: str) -> str:
    response = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "Mozilla/5.0",
        },
    )

    response.raise_for_status()

    return response.text


def parse_films(html: str) -> dict[str, dict]:
    soup = BeautifulSoup(html, "html.parser")

    films = {}

    film_cards = soup.select("article.product_pod")

    for card in film_cards:
        link_element = card.select_one("h3 a")

        relative_film_url = link_element["href"]
        film_key = relative_film_url.split("/")[-2]

        films[film_key] = {
            "title": link_element["title"],
            "director": UNKNOWN_DIRECTOR,
        }

    return films


def save_to_json(
    data: dict[str, dict],
    file_path: Path,
) -> None:
    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with file_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4,
        )


def main() -> None:
    html = get_page_html(PAGE_URL)
    films = parse_films(html)
    save_to_json(films, OUTPUT_FILE)

    print(f"Получено записей: {len(films)}")
    print(f"Данные сохранены в {OUTPUT_FILE}")


if __name__ == "__main__":
    main()