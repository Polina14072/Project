import sqlite3

films_data = {
    "titanik_3001": {"title": "Титаник", "director": "Джеймс Кэмерон"},
    "avengers-final_3002": {"title": "Мстители: Финал", "director": "Энтони и Джо Руссо"},
    "zvyozdnye-voyny-probuzhdenie-sily_3003": {"title": "Звёздные войны: Пробуждение силы", "director": "Дж. Дж. Абрамс"},
    "garri-potter-i-filosofskiy-kamen_3004": {"title": "Гарри Поттер и философский камень", "director": "Крис Коламбус"},
    "korol-lev_3005": {"title": "Король Лев", "director": "Роджер Аллерс, Роб Минкофф"},
    "temnyy-rytsar_3006": {"title": "Тёмный рыцарь", "director": "Кристофер Нолан"},
    "joker_3007": {"title": "Джокер", "director": "Тодд Филлипс"},
    "paraziti_3008": {"title": "Паразиты", "director": "Пон Джун-хо"},
    "forrest-gamp_3009": {"title": "Форрест Гамп", "director": "Роберт Земекис"},
    "shrek_3010": {"title": "Шрек", "director": "Эндрю Адамсон, Вики Дженсон"},
    "chelovek-pauk-net-puti-domoy_3011": {"title": "Человек-паук: Нет пути домой", "director": "Джон Уоттс"},
    "barbi_3012": {"title": "Барби", "director": "Грета Гервиг"},
    "oppengeymer_3013": {"title": "Оппенгеймер", "director": "Кристофер Нолан"},
    "la-la-lend_3014": {"title": "Ла-Ла Ленд", "director": "Дэмьен Шазелл"},
    "vsyo-vezde-i-srazu_3015": {"title": "Всё, везде и сразу", "director": "Дэниэл Кван, Дэниэл Шайнерт"},
    "znakomstvo-s-roditelyami_3016": {"title": "Знакомство с родителями", "director": "Джей Роуч"},
    "1plus1_3017": {"title": "1+1", "director": "Оливье Накаш, Эрик Толедано"},
    "krasavitsa-i-chudovische_3018": {"title": "Красавица и чудовище", "director": "Билл Кондон"},
    "otel-grand-budapesht_3019": {"title": "Отель «Гранд Будапешт»", "director": "Уэс Андерсон"},
    "zelyonaya-kniga_3020": {"title": "Зелёная книга", "director": "Питер Фаррелли"},
}

conn = sqlite3.connect("films.db")
cur = conn.cursor()

# Удаляем старые записи (книги), чтобы не смешивались с фильмами
cur.execute("DELETE FROM films")

for slug, data in films_data.items():
    cur.execute(
        "INSERT INTO films (title, director) VALUES (?, ?)",
        (data["title"], data["director"])
    )
    print(f"Добавлен фильм: {data['title']}")

conn.commit()
print(f"Готово. Добавлено: {len(films_data)}")
conn.close()